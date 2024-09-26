use std::process::{exit, Command, Stdio};

use crate::browsers::Browser;

pub fn open_url_in_browser(url: &str, browser: &Browser) {
    let exec_path = browser.exec.to_str().unwrap();
    let trimmed_exec = exec_path.trim();

    let result = if cfg!(target_os = "windows") {
        Command::new("cmd")
            .arg("/C") // /C 表示执行命令并退出
            .arg(format!("{} {}", trimmed_exec, url)) // 拼接命令
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .spawn()
    } else {
        Command::new(trimmed_exec)
            .arg(url)
            .stdout(Stdio::null())
            .stderr(Stdio::null())
            .spawn()
    };

    match result {
        Ok(_) => exit(0),
        Err(e) => {
            eprintln!("Failed to open URL in browser: {}", e);
        }
    }
}
