import os
from typing import Dict
import tomllib
from xdg import BaseDirectory
import tomli_w


class Config:
    def __init__(self, config_path: str = None):
        self.config_path = config_path or os.path.join(
            BaseDirectory.xdg_config_home, "linkwiz", "linkwiz.toml"
        )
        self._config = self._load_config()

    def _load_config(self) -> Dict:
        """
        Load the configuration file, creating a new one with defaults if it doesn't exist.
        """
        config_dir = os.path.dirname(self.config_path)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

        if os.path.exists(self.config_path):
            with open(self.config_path, "rb") as f:
                return tomllib.load(f)
        else:
            config = {
                "main": {"auto_find_browsers": True},
                "browsers": {},
                "rules": {"fnmatch": {}, "hostname": {}},
                "features": {"remove_track": False},
            }
            with open(self.config_path, "wb") as f:
                tomli_w.dump(config, f)
            return config

    def save_config(self):
        """
        Save the configuration file.
        """
        with open(self.config_path, "wb") as f:
            tomli_w.dump(self._config, f)

    def add_rules(self, hostname: str, browser_name: str):
        """
        Add rules to the configuration file.
        """
        if "rules" not in self._config:
            self._config["rules"] = {"regex": {}, "fnmatch": {}, "hostname": {}}
        rules = self._config["rules"]
        if "hostname" not in rules:
            rules["hostname"] = {}
        rules["hostname"][hostname] = browser_name
        self.save_config()

    @property
    def main(self) -> Dict:
        """
        Get the main section from the configuration.
        """
        return self._config.get("main", {})

    @property
    def browsers(self) -> Dict:
        """
        Get the browsers from the configuration.
        """
        return self._config.get("browsers", {})

    @property
    def rules(self) -> Dict:
        """
        Get the rules from the configuration.
        """
        return self._config.get("rules", {})

    @property
    def rules_fnmatch(self) -> Dict:
        """
        Get the fnmatch rules from the configuration.
        """
        return self.rules.get("fnmatch", {})

    @property
    def rules_hostname(self) -> Dict:
        """
        Get the hostname rules from the configuration.
        """
        return self.rules.get("hostname", {})

    @property
    def features(self) -> Dict:
        """
        Get the features from the configuration.
        """
        return self._config.get("features", {})


config = Config()
