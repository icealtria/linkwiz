use super::Choice;
use crate::{core::Browser, utils::hostname_port_from_url};
use eframe::egui;
use std::sync::mpsc::Sender;
use url::Url;

pub fn show_selector(browsers: Vec<Browser>, url: Url, tx: Sender<Choice>) {
    let mut browsers = browsers;
    browsers.sort_by(|a, b| a.name.to_lowercase().cmp(&b.name.to_lowercase()));

    let window_height = (browsers.len() * 30 + (browsers.len() + 2) * 3 + 50) as f32;
    let window_width = browsers
        .iter()
        .max_by(|a, b| a.name.len().cmp(&b.name.len()))
        .map(|b| b.name.len() as f32 * 8.0)
        .unwrap()
        .max(100.0)
        + 25.0;

    let options = eframe::NativeOptions {
        centered: true,
        viewport: eframe::egui::ViewportBuilder::default()
            .with_inner_size([window_width, window_height])
            // .with_resizable(false)
            .with_decorations(true),
        ..Default::default()
    };

    let _ = eframe::run_native(
        "Select",
        options,
        Box::new(move |_cc| {
            Ok(Box::new(BrowserSelectorApp {
                browsers,
                selected_browser: None,
                url,
                remember_choice: false,
                tx,
                copy_notification_time: None,
            }))
        }),
    );
}

struct BrowserSelectorApp {
    browsers: Vec<Browser>,
    selected_browser: Option<Browser>,
    url: Url,
    remember_choice: bool,
    tx: Sender<Choice>,
    copy_notification_time: Option<f64>,
}

impl eframe::App for BrowserSelectorApp {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        if let Some(time) = self.copy_notification_time {
            if ctx.input(|i| i.time) > time + 1.0 {
                self.copy_notification_time = None;
            }
        }

        egui::CentralPanel::default().show(ctx, |ui| {
            let truncated_url = truncate_url(&self.url);

            ui.horizontal(|ui| {
                let display_text = if let Some(copy_time) = self.copy_notification_time {
                    let current_time = ctx.input(|i| i.time);
                    if current_time - copy_time <= 1.0 {
                        "copied".to_string()
                    } else {
                        self.copy_notification_time = None;
                        truncated_url
                    }
                } else {
                    truncated_url
                };

                let label_resp = ui.add(egui::Label::new(&display_text).wrap());

                if label_resp.clicked() {
                    ui.output_mut(|o| o.copied_text = self.url.to_string());
                    self.copy_notification_time = Some(ctx.input(|i| i.time));
                }

                label_resp.on_hover_ui(|ui| {
                    ui.style_mut().interaction.selectable_labels = false;
                    ui.label(&self.url.to_string());
                });
            });

            let button_width = ui.available_width();
            let input = ui.input(|i| i.clone());
            let mut clicked_index: Option<usize> = None;

            for (i, browser) in self.browsers.iter().enumerate() {
                let button_text = format!("{}. {}", i + 1, browser.name);

                if ui
                    .add_sized([button_width, 30.0], egui::Button::new(&button_text))
                    .clicked()
                {
                    clicked_index = Some(i);
                }

                if (i + 1) <= 9 {
                    let key = match i {
                        0 => egui::Key::Num1,
                        1 => egui::Key::Num2,
                        2 => egui::Key::Num3,
                        3 => egui::Key::Num4,
                        4 => egui::Key::Num5,
                        5 => egui::Key::Num6,
                        6 => egui::Key::Num7,
                        7 => egui::Key::Num8,
                        8 => egui::Key::Num9,
                        _ => continue,
                    };
                    if input.key_pressed(key) {
                        clicked_index = Some(i);
                    }
                }
            }

            if let Some(i) = clicked_index {
                let selected_browser = self.browsers[i].clone();
                self.selected_browser = Some(selected_browser.clone());

                self.tx
                    .send(Choice {
                        browser: selected_browser,
                        is_remember: self.remember_choice,
                    })
                    .ok();

                ui.ctx().send_viewport_cmd(egui::ViewportCommand::Close);
            }

            if input.key_pressed(egui::Key::Q) {
                ui.ctx().send_viewport_cmd(egui::ViewportCommand::Close);
            }

            if input.key_pressed(egui::Key::R) {
                self.remember_choice = !self.remember_choice;
                ctx.request_repaint();
            }

            ui.horizontal(|ui| {
                let checkbox_width = 80.0;
                // let quit_button_width = 40.0;

                ui.add_sized(
                    egui::vec2(checkbox_width, 20.0),
                    egui::Checkbox::new(&mut self.remember_choice, "Remember"),
                );

                // ui.add_space(250.0 - checkbox_width - quit_button_width - 25.0);

                // if ui
                //     .add_sized(
                //         egui::vec2(quit_button_width, 20.0),
                //         egui::Button::new("Quit"),
                //     )
                //     .clicked()
                // {
                //     ui.ctx().send_viewport_cmd(egui::ViewportCommand::Close);
                // }
            });
        });
    }
}

fn truncate_url(url: &Url) -> String {
    let url_scheme = url.scheme();
    let host_port = hostname_port_from_url(url);

    if url.path().is_empty() || url.path() == "/" {
        format!("{}://{}{}", url_scheme, host_port, "/")
    } else {
        format!("{}://{}{}", url_scheme, host_port, "/~")
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_truncate_url() {
        let urls = vec![
            Url::parse("https://www.example.com").unwrap(),
            Url::parse("https://www.example.com/path").unwrap(),
            Url::parse("http://127.0.0.1:8080/").unwrap(),
            Url::parse("http://127.0.0.1:8080/path").unwrap(),
        ];

        let expected_output = vec![
            "https://www.example.com/",
            "https://www.example.com/~",
            "http://127.0.0.1:8080/",
            "http://127.0.0.1:8080/~",
        ];

        let output: Vec<String> = urls.iter().map(|url| truncate_url(url)).collect();

        assert_eq!(output, expected_output);
    }
}
