use std::process::{Command, Stdio};

use find_browsers::Browser;

#[cfg(target_os = "windows")]
use std::os::windows::process::CommandExt;

pub fn open_url_in_browser(url: &str, browser: &Browser) {
    let exec_path = browser.exec.to_str().unwrap();
    let trimmed_exec = exec_path.trim();

    let has_additional_args = trimmed_exec.contains(' ');

    #[cfg(target_os = "windows")]
    {
        if has_additional_args {
            Command::new("cmd")
                .creation_flags(0x08000000)
                .arg("/C")
                .arg(trimmed_exec)
                .arg(url)
                .stdout(Stdio::null())
                .stderr(Stdio::null())
                .spawn()
                .expect("Failed to open URL in browser");
        } else {
            Command::new(trimmed_exec)
                .creation_flags(0x08000000)
                .arg(url)
                .stdout(Stdio::null())
                .stderr(Stdio::null())
                .spawn()
                .expect("Failed to open URL in browser");
        }
    }

    #[cfg(target_os = "linux")]
    {
        if has_additional_args {
            Command::new("sh")
                .arg("-c")
                .arg(format!("{} {}", trimmed_exec, url))
                .stdout(Stdio::null())
                .stderr(Stdio::null())
                .spawn()
                .expect("Failed to open URL in browser");
        } else {
            Command::new(trimmed_exec)
                .arg(url)
                .stdout(Stdio::null())
                .stderr(Stdio::null())
                .spawn()
                .expect("Failed to open URL in browser");
        }
    }
}
