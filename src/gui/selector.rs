use crate::browsers::Browser;
use eframe::egui;
use std::sync::mpsc::Sender;
use url::Url;

use super::Choice;

pub fn show_selector(browsers: Vec<Browser>, url: Url, tx: Sender<Choice>) {
    let _ = eframe::run_native(
        "Select a Browser",
        eframe::NativeOptions::default(),
        Box::new(move |_cc| {
            Ok(Box::new(BrowserSelectorApp {
                browsers,
                selected_browser: None,
                url: url.to_string(),
                remember_choice: false,
                tx,
            }))
        }),
    );
}
struct BrowserSelectorApp {
    browsers: Vec<Browser>,
    selected_browser: Option<Browser>,
    url: String,
    remember_choice: bool,
    tx: Sender<Choice>,
}

impl eframe::App for BrowserSelectorApp {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        egui::CentralPanel::default().show(ctx, |ui| {
            ui.label(self.url.clone());
            for browser in &self.browsers {
                if ui.button(&browser.name).clicked() {
                    let selected_browser = browser.clone();
                    self.selected_browser = Some(selected_browser.clone());

                    self.tx
                        .send(Choice {
                            browser: selected_browser,
                            is_remember: self.remember_choice,
                        })
                        .ok();

                    ui.ctx().send_viewport_cmd(egui::ViewportCommand::Close);
                }
            }
            ui.checkbox(&mut self.remember_choice, "Remember");
        });
    }
}
