use std::process::{exit, Command, Stdio};

use crate::browsers::Browser;

pub fn open_url_in_browser(url: &str, browser: &Browser) {
    let exec_path = browser.exec.to_str().unwrap();

    let trimmed_exec = exec_path.trim();
    match Command::new(trimmed_exec)
        .arg(url)
        .stdout(Stdio::null())
        .stderr(Stdio::null())
        .spawn()
    {
        Ok(_) => exit(0),
        Err(e) => eprintln!("Failed to execute command: {}", e),
    }
}
