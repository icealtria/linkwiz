use crate::{
    browsers::{self, Browser},
    config::Config,
    matching,
};
use url::Url;

pub fn process_url(url: &str) {
    let parsed_url = Url::parse(url).expect("Invalid URL");

    if !["http", "https"].contains(&parsed_url.scheme()) {
        panic!("Invalid URL scheme.");
    }

    let mut config = Config::new();

    let mut browsers = browsers::get_browsers();

    let conf_browsers = config
        .browsers
        .iter()
        .map(|(name, exec)| Browser {
            name: name.clone(),
            exec: exec.clone().into(),
        })
        .collect::<Vec<Browser>>();

    browsers.extend(conf_browsers);

    let hostname = parsed_url.host_str().expect("Invalid URL.");

    match matching::match_hostname(&browsers, &hostname, &config.rules) {
        Some(browser) => {
            crate::launch::open_url_in_browser(&parsed_url.to_string(), &browser);
        }
        None => {
            let choice = crate::gui::open_with_selector(browsers, parsed_url.clone());
            if let Some(choice) = choice {
                if choice.is_remember {
                    config.add_rules(hostname.to_string(), choice.browser.name.clone());
                }
                crate::launch::open_url_in_browser(&parsed_url.to_string(), &choice.browser);
            }
        }
    }
}
