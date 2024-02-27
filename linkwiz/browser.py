import configparser
from pathlib import Path
from typing import Dict, Set
from dataclasses import dataclass

from xdg import BaseDirectory, DesktopEntry

from linkwiz.config import custom_browsers

APPNAME: str = "LinkWiz"
MIMEAPPS_LIST_FILE: str = "mimeapps.list"
HTTP_HANDLER: str = "x-scheme-handler/http"
HTTPS_HANDLER: str = "x-scheme-handler/https"

DESKTOP_PATHS = [
    Path("/usr/share/applications/"),
    Path.home() / ".local/share/applications/",
]


@dataclass
class Browser:
    """Data class to represent a browser."""

    name: str
    exec_path: Path


def get_mimeapps_list_path() -> Path:
    """Get the path of mimeapps.list file."""
    return BaseDirectory.load_first_config(MIMEAPPS_LIST_FILE)


def parse_mimeapps_list() -> configparser.ConfigParser:
    """Parse the mimeapps.list file."""
    config: configparser.ConfigParser = configparser.ConfigParser()
    config.read(get_mimeapps_list_path())
    return config


def get_installed_browsers() -> Dict[str, Path]:
    """Get a dictionary of installed browsers."""
    config: configparser.ConfigParser = parse_mimeapps_list()
    handlers = [
        config["Added Associations"].get(handler, "").split(";")
        for handler in (HTTP_HANDLER, HTTPS_HANDLER)
    ]
    browser_desktop_entries: Set[str] = set(handlers[0]) & set(handlers[1])
    browser_desktop_entries.discard(f"{APPNAME.lower()}.desktop")
    return get_browser_entry(browser_desktop_entries)


def get_browser_entry(browser_desktop_entries: Set[str]) -> Dict[str, Path]:
    """Check and validate browsers in the mimeapps.list file."""
    installed_browsers: Dict[str, Path] = {}
    for path in DESKTOP_PATHS:
        if path.exists():
            for entry in path.iterdir():
                if entry.name in browser_desktop_entries:
                    desktop_entry: DesktopEntry.DesktopEntry = (
                        DesktopEntry.DesktopEntry(str(entry))
                    )
                    name: str = desktop_entry.getName()
                    execpath: str = desktop_entry.getExec()
                    installed_browsers[name] = Path(execpath)
    installed_browsers.update(custom_browsers)
    return installed_browsers
