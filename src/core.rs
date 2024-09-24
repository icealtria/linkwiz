use crate::{browsers, config::Config, matching};
use url::Url;

pub fn process_url(url: &str) {
    let parsed_url = Url::parse(url).expect("Invalid URL");

    if !["http", "https"].contains(&parsed_url.scheme()) {
        panic!("Invalid URL scheme.");
    }

    let config = Config::new();

    let browsers = browsers::get_browsers();

    match matching::match_url(browsers, &parsed_url, config.rules) {
        Some(browser) => {
            let mut command = std::process::Command::new(browser.exec.as_os_str());
            command.arg(url);
            command.spawn().expect("Failed to open URL in browser.");
        }
        None => {
            println!("No matching browser found for the URL.");
        }
    }
}
