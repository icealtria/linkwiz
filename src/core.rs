use crate::{config::Config, matching, utils::hostname_port_from_url};
#[cfg(target_os = "linux")]
use find_browsers::get_executable_browsers;
#[cfg(target_os = "windows")]
use find_browsers::get_browsers;
use serde::{Deserialize, Serialize};
use url::Url;

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Browser {
    pub name: String,
    pub exec: Vec<String>,
}

pub fn process_url(url: &str) {
    match try_process_url(url) {
        Ok(_) => {}
        Err(e) => crate::gui::error::show_error(&e.to_string()),
    }
}

fn try_process_url(url: &str) -> Result<(), Box<dyn std::error::Error>> {
    let parsed_url = Url::parse(url)?;

    if !["http", "https"].contains(&parsed_url.scheme()) {
        return Err("Invalid URL scheme".into());
    }

    let mut config = Config::new()?;

    #[cfg(target_os = "linux")]
    let browsers = get_executable_browsers().map_err(|e| format!("Failed to get browsers: {}", e))?;

    #[cfg(target_os = "windows")]
    let browsers = get_browsers().map_err(|e| format!("Failed to get browsers: {}", e))?;
    
    let mut browsers = browsers
        .iter()
        .map(|browser| {
            let exec: Vec<String> = vec![browser.exec.display().to_string()];
            Browser {
                name: browser.name.clone(),
                exec,
            }
        })
        .collect::<Vec<Browser>>();

    browsers = remove_self(browsers);

    let conf_browsers: Vec<Browser> = config
        .browsers
        .iter()
        .map(|(name, exec)| Browser {
            name: name.clone(),
            exec: exec.clone().into(),
        })
        .collect::<Vec<Browser>>();

    browsers.extend(conf_browsers);

    let hostname = hostname_port_from_url(&parsed_url);

    match matching::match_hostname(&browsers, &hostname, &config.rules) {
        Some(browser) => crate::launch::open_url_in_browser(&parsed_url.to_string(), &browser)?,
        None => match config.features.default_browser {
            Some(default_browser) => {
                let default_browser = browsers
                    .iter()
                    .find(|browser| browser.name == default_browser)
                    .ok_or("Default browser not found")?;
                crate::launch::open_url_in_browser(&parsed_url.to_string(), &default_browser)?
            }
            None => {
                let choice: Option<crate::gui::Choice> =
                    crate::gui::open_with_selector(browsers, parsed_url.clone());
                if let Some(choice) = choice {
                    if choice.is_remember {
                        config.add_rules(hostname.to_string(), choice.browser.name.clone())?;
                    }
                    crate::launch::open_url_in_browser(&parsed_url.to_string(), &choice.browser)?;
                } else {
                    println!("No browser selected")
                }
            }
        },
    }
    Ok(())
}

fn remove_self(browsers: Vec<Browser>) -> Vec<Browser> {
    browsers
        .iter()
        .filter(|browser| browser.name.to_lowercase() != "linkwiz")
        .cloned()
        .collect()
}
