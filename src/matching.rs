use crate::{browsers::Browser, config::RulesConfig};
use wildmatch::WildMatch;

pub fn match_hostname(
    browsers: &Vec<Browser>,
    hostname: &str,
    config: &RulesConfig,
) -> Option<Browser> {
    let fnmatch_browser = config.fnmatch.iter().find_map(|(pattern, browser)| {
        if WildMatch::new(pattern).matches(hostname) {
            Some(browser)
        } else {
            None
        }
    });

    let matched_browser = fnmatch_browser.or_else(|| config.hostname.get(hostname));

    matched_browser.and_then(|browser_name| {
        browsers
            .iter()
            .find(|browser| &browser.name == browser_name)
            .cloned()
    })
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::{collections::HashMap, path::PathBuf};

    #[test]
    fn test_match_url() {
        let browsers = vec![
            Browser {
                name: "Firefox".to_string(),
                exec: PathBuf::from("C:\\Program Files\\Mozilla Firefox\\firefox.exe"),
            },
            Browser {
                name: "Chrome".to_string(),
                exec: PathBuf::from("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"),
            },
        ];

        let config = RulesConfig {
            hostname: HashMap::new(),
            fnmatch: HashMap::from([
                ("*.example.com".to_string(), "Firefox".to_string()),
                ("*.cn".to_string(), "Chrome".to_string()),
            ]),
        };

        let hostnames = ["www.example.com", "189.cn"];

        let expected_results = [Some("Firefox".to_string()), Some("Chrome".to_string())];

        let results: Vec<Option<String>> = hostnames
            .iter()
            .map(|&hostname| {
                match_hostname(&browsers, hostname, &config).map(|browser| browser.name)
            })
            .collect();

        assert_eq!(results, expected_results);
    }
}
