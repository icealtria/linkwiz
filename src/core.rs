use crate::{browsers, config::Config, matching};
use std::process::{exit, Command, Stdio};
use url::Url;

pub fn process_url(url: &str) {
    let parsed_url = Url::parse(url).expect("Invalid URL");

    if !["http", "https"].contains(&parsed_url.scheme()) {
        panic!("Invalid URL scheme.");
    }

    let config = Config::new();

    let browsers = browsers::get_browsers();

    let hostname = parsed_url.host_str().expect("Invalid URL.");

    match matching::match_hostname(&browsers, &hostname, &config.rules) {
        Some(browser) => {
            println!(
                "Opening {} in browser: {}",
                parsed_url.as_str(),
                browser.name
            );

            let exec_path = browser.exec.to_str().unwrap();

            let trimmed_exec = exec_path.trim();

            match Command::new(trimmed_exec)
                .arg(parsed_url.as_str())
                .stdout(Stdio::null())
                .stderr(Stdio::null())
                .spawn()
            {
                Ok(_) => exit(0),
                Err(e) => eprintln!("Failed to execute command: {}", e),
            }
        }
        None => {
            println!("No matching browser found for the URL.");
        }
    }
}
