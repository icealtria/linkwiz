use crate::{
    config::Config,
    matching, utils::hostname_port_from_url,
};
use find_browsers::{get_browsers, Browser};
use url::Url;

pub fn process_url(url: &str) {
    let parsed_url = Url::parse(url).expect("Invalid URL");

    if !["http", "https"].contains(&parsed_url.scheme()) {
        panic!("Invalid URL scheme.");
    }

    let mut config = Config::new();

    let mut browsers = get_browsers().unwrap();

    let conf_browsers = config
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
        Some(browser) => {
            crate::launch::open_url_in_browser(&parsed_url.to_string(), &browser);
        }
        None => match config.features.default_browser {
            Some(default_browser) => {
                let default_browser = browsers
                    .iter()
                    .find(|browser| browser.name == default_browser)
                    .expect("Default browser not found");
                crate::launch::open_url_in_browser(&parsed_url.to_string(), &default_browser);
            }
            None => {
                let choice: Option<crate::gui::Choice> =
                    crate::gui::open_with_selector(browsers, parsed_url.clone());
                if let Some(choice) = choice {
                    if choice.is_remember {
                        config.add_rules(hostname.to_string(), choice.browser.name.clone());
                    }
                    crate::launch::open_url_in_browser(&parsed_url.to_string(), &choice.browser);
                }
            }
        },
    }
}