use crate::core::Browser;
use std::process::{Command, Stdio};

pub fn open_url_in_browser(url: &str, browser: &Browser) {
    let mut args = browser.exec.clone();
    args.push(url.to_string());

    #[cfg(any(target_os = "windows", target_os = "linux"))]
    {
        Command::new(args[0].clone())
            .args(&args[1..])
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .spawn()
            .expect("Failed to open URL in browser");
    }

    #[cfg(not(any(target_os = "windows", target_os = "linux")))]
    {
        unimplemented!("Browser launching is not implemented for this operating system");
    }
}
