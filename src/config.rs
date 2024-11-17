use dirs::config_dir;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs;
use std::path::{Path, PathBuf};

#[derive(Serialize, Deserialize, Debug)]
pub struct Config {
    pub browsers: HashMap<String, Vec<String>>,
    pub rules: RulesConfig,
    pub features: FeaturesConfig,
}

#[derive(Serialize, Deserialize, Debug, Default)]
pub struct RulesConfig {
    pub fnmatch: HashMap<String, String>,
    pub hostname: HashMap<String, String>,
}

#[derive(Serialize, Deserialize, Debug, Default)]
pub struct FeaturesConfig {
    pub default_browser: Option<String>,
}

impl Default for Config {
    fn default() -> Self {
        Config {
            browsers: HashMap::new(),
            rules: RulesConfig {
                fnmatch: HashMap::new(),
                hostname: HashMap::new(),
            },
            features: FeaturesConfig::default(),
        }
    }
}

impl Config {
    pub fn new() -> Result<Self, Box<dyn std::error::Error>> {
        let config_path = Self::config_path();
        if config_path.exists() {
            let config_data = fs::read_to_string(&config_path)?;
            Ok(toml::from_str(&config_data)?)
        } else {
            let config = Config::default();
            config.save(&config_path)?;
            Ok(config)
        }
    }

    fn save(&self, config_path: &Path) -> Result<(), Box<dyn std::error::Error>> {
        let toml_data = toml::to_string(&self)?;
        let config_dir = config_path.parent().unwrap();
        if !config_dir.exists() {
            fs::create_dir_all(config_dir)?;
        }
        fs::write(config_path, toml_data)?;
        Ok(())
    }

    fn config_path() -> PathBuf {
        let mut path = config_dir().unwrap_or_else(|| PathBuf::from("."));
        path.push("linkwiz");
        path.push("linkwiz.toml");
        path
    }

    pub fn add_rules(&mut self, hostname: String, browser_name: String) -> Result<(), Box<dyn std::error::Error>> {
        self.rules.hostname.insert(hostname, browser_name);
        self.save(&Self::config_path())?;
        Ok(())
    }
}
