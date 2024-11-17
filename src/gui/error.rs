use eframe::{self, egui};

pub fn show_error(message: String) {
    let native_options = eframe::NativeOptions {
        centered: true,
        viewport: eframe::egui::ViewportBuilder::default()
            .with_inner_size([300.0, 100.0])
            .with_resizable(false)
            .with_decorations(true),
        ..Default::default()
    };

    eframe::run_native(
        "Error",
        native_options,
        Box::new(|_cc| Ok(Box::new(ErrorWindow::new(message)))),
    )
    .ok();
}

struct ErrorWindow {
    message: String,
}

impl ErrorWindow {
    fn new(message: String) -> Self {
        Self { message }
    }
}

impl eframe::App for ErrorWindow {
    fn update(&mut self, ctx: &egui::Context, _: &mut eframe::Frame) {
        egui::CentralPanel::default().show(ctx, |ui| {
            ui.vertical_centered(|ui| {
                ui.label(&self.message);
                ui.add_space(10.0);
            });
        });
    }
}
