import os
from typing import Dict
from tomlkit import parse, dumps
from tomlkit.toml_document import TOMLDocument
from xdg import BaseDirectory


class Config:
    def __init__(self, config_path: str = None):
        self.config_path = config_path or os.path.join(
            BaseDirectory.xdg_config_home, "linkwiz.toml"
        )
        self._config = self._load_config()

    def _load_config(self) -> TOMLDocument:
        """
        Load the configuration file, creating a new one with defaults if it doesn't exist.
        """
        if os.path.exists(self.config_path):
            with open(self.config_path, "r") as f:
                return parse(f.read())
        else:
            config = TOMLDocument()
            config.add("browsers", {})
            config.add("rules", {"regex": {}, "hostname": {}})
            with open(self.config_path, "w") as f:
                f.write(dumps(config))
            return config

    def save_config(self):
        """
        Save the configuration file.
        """
        with open(self.config_path, "w") as f:
            f.write(dumps(self._config))

    def add_rules(self, hostname: str, browser_name: str):
        """
        Add rules to the configuration file.
        """
        if "rules" not in self._config:
            self._config.add("rules", {"regex": {}, "hostname": {}})
        rules = self._config["rules"]
        if "hostname" not in rules:
            rules["hostname"] = {}
        rules["hostname"][hostname] = browser_name
        self.save_config()

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
    def rules_regex(self) -> Dict:
        """
        Get the regex rules from the configuration.
        """
        return self.rules.get("regex", {})

    @property
    def rules_hostname(self) -> Dict:
        """
        Get the hostname rules from the configuration.
        """
        return self.rules.get("hostname", {})


config = Config()

custom_browsers = config.browsers
rules = config.rules
rules_regex = config.rules_regex
rules_hostname = config.rules_hostname
