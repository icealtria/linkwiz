pub struct Choice {
    pub browser: Browser,
    pub is_remember: bool,
}

use crate::browsers::Browser;
use std::sync::mpsc;
use url::Url;

pub mod selector;

pub fn open_with_selector(browsers: Vec<Browser>, url: Url) -> Option<Choice> {
    let (tx, rx) = mpsc::channel();

    selector::show_selector(browsers, url, tx);

    match rx.recv() {
        Ok(choice) => Some(choice),
        Err(_) => None,
    }
}