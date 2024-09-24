use dirs::home_dir;
use std::fs;
use std::path::{Path, PathBuf};

use super::Browser;

const SELF_DESKTOP: &str = "linkwiz.desktop";
const HTTP_HANDLER: &str = "x-scheme-handler/http";

const SYSTEM_DESKTOP_PATH: &str = "/usr/share/applications/";
const LOCAL_DESKTOP_PATH: &str = ".local/share/applications/";
const SYSTEM_MIMEINFO_PATH: &str = "/usr/share/applications/mimeinfo.cache";
const LOCAL_MIMEINFO_PATH: &str = ".local/share/applications/mimeinfo.cache";

pub fn get_browsers() -> Vec<Browser> {
    match find_installed_browsers() {
        Ok(browser_names) => resolve_browser_exec_paths(&browser_names),
        Err(e) => {
            eprintln!("Error: {}", e);
            std::process::exit(1);
        }
    }
}

fn find_installed_browsers() -> Result<Vec<String>, std::io::Error> {
    let mut installed_browsers: Vec<String> = Vec::new();

    for mimeinfo_path in get_mimeinfo_paths() {
        if !mimeinfo_path.exists() {
            continue;
        }

        let file_content = fs::read_to_string(&mimeinfo_path)?;
        extract_browsers_from_mimeinfo(&file_content, &mut installed_browsers);
    }

    installed_browsers.retain(|b: &String| b != SELF_DESKTOP);
    Ok(installed_browsers)
}

fn get_mimeinfo_paths() -> Vec<PathBuf> {
    let mut paths = vec![PathBuf::from(SYSTEM_MIMEINFO_PATH)];

    if let Some(home) = home_dir() {
        let local_mimeinfo = home.join(LOCAL_MIMEINFO_PATH);
        paths.push(local_mimeinfo);
    }

    paths
}

fn extract_browsers_from_mimeinfo(content: &str, installed_browsers: &mut Vec<String>) {
    for line in content.lines() {
        if line.starts_with(HTTP_HANDLER) {
            let browsers: Vec<String> = line
                .split('=')
                .nth(1)
                .unwrap_or("")
                .trim()
                .split(';')
                .map(|s| s.to_string())
                .collect();
            installed_browsers.extend(browsers);
            break;
        }
    }
}

fn resolve_browser_exec_paths(browser_names: &[String]) -> Vec<Browser> {
    let mut browsers_exec: Vec<Browser> = Vec::new();

    for desktop_path in get_desktop_paths() {
        if !desktop_path.exists() {
            continue;
        }

        for entry in fs::read_dir(desktop_path).unwrap_or_else(|_| fs::read_dir("/").unwrap()) {
            if let Ok(entry) = entry {
                let entry_path = entry.path();
                if let Some(file_name) = entry_path.file_name().and_then(|s| s.to_str()) {
                    if browser_names.contains(&file_name.to_string()) {
                        if let Some(browser) = parse_desktop_entry(&entry_path) {
                            browsers_exec.push(browser);
                        }
                    }
                }
            }
        }
    }

    browsers_exec
}

fn get_desktop_paths() -> Vec<PathBuf> {
    let mut paths = vec![PathBuf::from(SYSTEM_DESKTOP_PATH)];

    if let Some(home) = home_dir() {
        let local_desktop_path = home.join(LOCAL_DESKTOP_PATH);
        paths.push(local_desktop_path);
    }

    paths
}

fn parse_desktop_entry(path: &Path) -> Option<Browser> {
    let content = fs::read_to_string(path).ok()?;

    let name = extract_field_from_desktop_file("Name=", &content)?;
    let exec = extract_field_from_desktop_file("Exec=", &content)?;

    Some(Browser {
        name,
        exec: PathBuf::from(exec),
    })
}

fn extract_field_from_desktop_file(prefix: &str, content: &str) -> Option<String> {
    for line in content.lines() {
        if line.starts_with(prefix) {
            return Some(line.trim_start_matches(prefix).to_string());
        }
    }
    None
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn print_browsers() {
        let browsers = get_browsers();
        for browser in &browsers {
            println!("Browser: {}, Exec: {:?}", browser.name, browser.exec);
        }
        assert!(!browsers.is_empty(), "No browsers found");
    }

    #[test]
    fn print_mimeinfo_content() {
        println!("{:?}", find_installed_browsers().unwrap());
        assert!(true);
    }
}
