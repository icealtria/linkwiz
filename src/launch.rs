use std::os::windows::process::CommandExt;
use std::process::{Command, Stdio};

use crate::browsers::Browser;

pub fn open_url_in_browser(url: &str, browser: &Browser) {
    let exec_path = browser.exec.to_str().unwrap();
    let trimmed_exec = exec_path.trim();

    let has_additional_args = trimmed_exec.contains(' ');

    let _ = if cfg!(target_os = "windows") {
        if has_additional_args {
            Command::new("cmd")
                .creation_flags(0x08000000)
                .arg("/C")
                .arg(trimmed_exec)
                .arg(url)
                .stdout(Stdio::null())
                .stderr(Stdio::null())
                .spawn()
        } else {
            Command::new(trimmed_exec)
                .creation_flags(0x08000000)
                .arg(url)
                .stdout(Stdio::null())
                .stderr(Stdio::null())
                .spawn()
        }
    } else {
        if has_additional_args {
            Command::new("sh")
                .arg("-c")
                .arg(format!("{} {}", trimmed_exec, url))
                .stdout(Stdio::null())
                .stderr(Stdio::null())
                .spawn()
        } else {
            Command::new(trimmed_exec)
                .arg(url)
                .stdout(Stdio::null())
                .stderr(Stdio::null())
                .spawn()
        }
    };
}
