import subprocess
from xdg import BaseDirectory, DesktopEntry
import configparser
from pathlib import Path

APPNAME = ""
MIMEAPPS_LIST_FILE = "mimeapps.list"
DESKTOP_PATHS = [
    Path("/usr/share/applications/"),
    Path.home() / ".local/share/applications/",
]
HTTP_HANDLER = "x-scheme-handler/http"
HTTPS_HANDLER = "x-scheme-handler/https"


def get_mimeapps_list_path():
    return BaseDirectory.load_first_config(MIMEAPPS_LIST_FILE)


def parse_mimeapps_list():
    config = configparser.ConfigParser()
    config.read(get_mimeapps_list_path())
    return config


def get_installed_browsers():
    """Get a dictionary of installed browsers."""
    config = configparser.ConfigParser()
    config.read(get_mimeapps_list_path())
    handlers = [
        config["Added Associations"].get(handler, "").split(";")
        for handler in (HTTP_HANDLER, HTTPS_HANDLER)
    ]
    browser_desktop_entries = set(handlers[0]) & set(handlers[1])

    return check_browser_valid(browser_desktop_entries)


def check_browser_valid(browser_desktop_entries):
    installed_browsers = {}
    for path in DESKTOP_PATHS:
        if path.exists():
            for entry in path.iterdir():
                if entry.name in browser_desktop_entries:
                    desktop_entry = DesktopEntry.DesktopEntry(str(entry))
                    name = desktop_entry.getName()
                    execpath = desktop_entry.getExec()
                    installed_browsers[name] = execpath
    return installed_browsers


def exec_field_to_cmds(exe: str, link):
    """
    >>> exec_field_to_cmds("firefox %u", "https://google.com")
    ['firefox', 'https://google.com']
    >>> exec_field_to_cmds("/usr/lib/firefox-developer-edition/firefox %u", "https://google.com")
    ['/usr/lib/firefox-developer-edition/firefox', 'https://google.com']
    """
    return exe.replace("%u", link).replace("%U", link).split()


def install():
    pass


def uninstall():
    pass


def open_link(exe, link):
    cmd = exec_field_to_cmds(exe, link)
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
