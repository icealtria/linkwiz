use crate::browsers::Browser;
use eframe::egui;
use std::sync::mpsc::Sender;
use url::Url;

use super::Choice;

pub fn show_selector(browsers: Vec<Browser>, url: Url, tx: Sender<Choice>) {
    let mut browsers = browsers;
    browsers.sort_by(|a, b| a.name.to_lowercase().cmp(&b.name.to_lowercase()));

    // Calculate the optimal window height based on the number of browsers
    let window_height = (20 + browsers.len() * 36 + 20) as f32; // Each button ~36px + padding

    let options = eframe::NativeOptions {
        viewport: eframe::egui::ViewportBuilder::default()
            .with_inner_size([250.0, window_height])
            .with_resizable(false),
        ..Default::default()
    };

    let _ = eframe::run_native(
        "Select a Browser",
        options,
        Box::new(move |_cc| {
            Ok(Box::new(BrowserSelectorApp {
                browsers,
                selected_browser: None,
                url,
                remember_choice: false,
                tx,
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
}

impl eframe::App for BrowserSelectorApp {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        egui::CentralPanel::default().show(ctx, |ui| {
            let truncated_url = truncate_url(&self.url);

            // Display the truncated URL and show the full URL on hover
            ui.horizontal(|ui| {
                ui.label(egui::RichText::new(&truncated_url))
                    .on_hover_text(self.url.to_string()); // Display the full URL on hover
            });

            // Define a button width for all buttons
            let button_width = ui.available_width();

            // Track keyboard input
            let input = ui.input(|i| i.clone());

            let mut clicked_index: Option<usize> = None;

            // Display browsers with index, sorted alphabetically
            for (i, browser) in self.browsers.iter().enumerate() {
                let button_text = format!("{}. {}", i + 1, browser.name);

                // Handle button press or keyboard input
                if ui
                    .add_sized([button_width, 30.0], egui::Button::new(&button_text))
                    .clicked()
                {
                    clicked_index = Some(i);
                }

                // Check for corresponding number key pressed (1-9)
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

            // If any browser is selected via button or keyboard
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

            // Checkbox for "Remember"
            ui.checkbox(&mut self.remember_choice, "Remember");
        });
    }
}

fn truncate_url(url: &Url) -> String {
    let url_scheme = url.scheme();
    let url_domain = url.domain().unwrap_or("");
    if url.path().is_empty() || url.path() == "/" {
        format!("{}://{}/", url_scheme, url_domain)
    } else {
        format!("{}://{}/~", url_scheme, url_domain)
    }
}
