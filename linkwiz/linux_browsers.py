import logging
from pathlib import Path
import subprocess
from typing import List
from xdg import DesktopEntry
from linkwiz.config import config
from linkwiz.types import BrowserExecs

SELF_DESKTOP: str = "linkwiz.desktop"
HTTP_HANDLER: str = "x-scheme-handler/http"

DESKTOP_PATHS: List[Path] = [
    Path("/usr/share/applications/"),
    Path.home() / ".local/share/applications/",
]

MIMEINFO_PATHS: List[Path] = [
    Path("/usr/share/applications/mimeinfo.cache"),
    Path.home() / ".local/share/applications/mimeinfo.cache",
]


def get_browsers() -> BrowserExecs:
    """Get the name and exec path of browsers."""
    try:
        installed_browsers: List[str] = []
        if config.main.get("auto_find_browsers", True):
            installed_browsers = find_installed_browsers()

        browsers: BrowserExecs = get_browser_exec(installed_browsers)
        return browsers
    except subprocess.CalledProcessError:
        logging.error("Error getting installed browsers")
        exit(1)


def find_installed_browsers() -> List[str]:
    """Get the name of installed browsers."""
    installed_browsers: set[str] = set()
    for path in MIMEINFO_PATHS:
        if not path.exists():
            continue
        with open(path, "r") as f:
            for line in f:
                if not line.startswith(HTTP_HANDLER):
                    continue
                browsers: List[str] = line.split("=")[-1].strip().split(";")
                installed_browsers.update(browsers)
                break
    installed_browsers.discard(SELF_DESKTOP)
    return list(installed_browsers)


def get_browser_exec(browsers_desktop: List[str]) -> BrowserExecs:
    """Get the exec path of installed browsers."""
    browsers_exec: BrowserExecs = {}
    for path in DESKTOP_PATHS:
        if not path.exists():
            continue
        for entry in path.glob("*.desktop"):
            if entry.name not in browsers_desktop:
                continue
            desktop_entry = DesktopEntry.DesktopEntry(str(entry))
            name: str = desktop_entry.getName()
            execpath: str = desktop_entry.getExec()
            browsers_exec[name] = Path(execpath)
    return browsers_exec
