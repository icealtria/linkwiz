use crate::browsers::Browser;
use std::collections::HashMap;
use std::path::PathBuf;
use winreg::enums::*;
use winreg::RegKey;
use winreg::HKEY;

pub fn get_browsers() -> Vec<Browser> {
    let mut browser_map = HashMap::new();

    if let Ok(installed_browsers) = read_browsers_from_registry(HKEY_LOCAL_MACHINE) {
        for browser in installed_browsers {
            browser_map.insert(browser.name.clone(), browser);
        }
    }

    if let Ok(installed_browsers) = read_browsers_from_registry(HKEY_CURRENT_USER) {
        for browser in installed_browsers {
            browser_map.insert(browser.name.clone(), browser);
        }
    }

    browser_map.into_values().collect()
}

fn read_browsers_from_registry(hkey: HKEY) -> Result<Vec<Browser>, Box<dyn std::error::Error>> {
    let base_key = RegKey::predef(hkey).open_subkey("SOFTWARE\\Clients\\StartMenuInternet")?;
    let mut browsers = Vec::new();

    for browser_name in base_key.enum_keys().filter_map(Result::ok) {
        // Skip Internet Explorer
        if browser_name.to_uppercase().contains("IEXPLORE") {
            continue;
        }

        let browser_key = base_key.open_subkey(&browser_name)?;

        let app_name: String = browser_key
            .get_value("")
            .unwrap_or_else(|_| browser_name.clone());

        let command_key = browser_key.open_subkey("shell\\open\\command")?;
        let command: String = command_key.get_value("")?;

        let exec_path = extract_executable_path(&command);

        browsers.push(Browser {
            name: app_name,
            exec: PathBuf::from(exec_path),
        });
    }

    Ok(browsers)
}

fn extract_executable_path(command: &str) -> String {
    if let Some(start) = command.find('"') {
        if let Some(end) = command[start + 1..].find('"') {
            return command[start + 1..start + 1 + end].to_string();
        }
    }

    command.split_whitespace().next().unwrap_or("").to_string()
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
}
