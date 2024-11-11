use find_browsers::Browser;
use std::process::{Command, Stdio};

#[cfg(target_os = "windows")]
use std::os::windows::process::CommandExt;

pub fn open_url_in_browser(url: &str, browser: &Browser) {
    let exec_path = browser.exec.to_str().unwrap();
    let encoded_url = url.replace("&", "%26");

    #[cfg(target_os = "windows")]
    {
        Command::new("cmd")
            .creation_flags(0x08000000)
            .arg("/C")
            .arg(exec_path)
            .arg(encoded_url)
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .spawn()
            .expect("Failed to open URL in browser");
    }

    #[cfg(target_os = "linux")]
    {
        Command::new("sh")
            .arg("-c")
            .arg(format!("{} {}", exec_path, encoded_url))
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .spawn()
            .expect("Failed to open URL in browser");
    }
}
