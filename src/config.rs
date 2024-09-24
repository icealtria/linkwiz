use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;
use std::path::{Path, PathBuf};
use dirs::config_dir;

#[derive(Serialize, Deserialize, Debug)]
pub struct Config {
    pub browsers: HashMap<String, String>,
    pub rules: RulesConfig,
}

#[derive(Serialize, Deserialize, Debug, Default)]
pub struct RulesConfig {
    pub fnmatch: HashMap<String, String>,
    pub hostname: HashMap<String, String>,
}
impl Default for Config {
    fn default() -> Self {
        Config {
            browsers: HashMap::new(),
            rules: RulesConfig {
                fnmatch: HashMap::new(),
                hostname: HashMap::new(),
            },
        }
    }
}

impl Config {
    pub fn new() -> Self {
        let config_path = {
            let mut path = config_dir().unwrap_or_else(|| PathBuf::from("."));
            path.push("linkwiz");
            path.push("linkwiz.toml");
            path
        };

        if config_path.exists() {
            let config_data = fs::read_to_string(&config_path).expect("Failed to read config file");
            toml::from_str(&config_data).expect("Failed to parse config file")
        } else {
            let config = Config::default();
            config.save(&config_path);
            config
        }
    }

    pub fn save(&self, config_path: &Path) {
        let toml_data = toml::to_string(&self).expect("Failed to serialize config");
        let config_dir = config_path.parent().unwrap();
        if !config_dir.exists() {
            fs::create_dir_all(config_dir).expect("Failed to create config directory");
        }
        fs::write(config_path, toml_data).expect("Failed to write config file");
    }

    pub fn add_rules(&mut self, hostname: String, browser_name: String) {
        self.rules.hostname.insert(hostname, browser_name);
    }
}
