pub struct Choice {
    pub browser: Browser,
    pub is_remember: bool,
}

use std::sync::mpsc;
use url::Url;

use crate::core::Browser;

pub mod selector;

pub fn open_with_selector(browsers: Vec<Browser>, url: Url) -> Option<Choice> {
    let (tx, rx) = mpsc::channel();

    selector::show_selector(browsers, url, tx);

    match rx.recv() {
        Ok(choice) => Some(choice),
        Err(_) => None,
    }
}

pub mod error;
