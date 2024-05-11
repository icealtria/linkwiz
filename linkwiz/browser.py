import logging
from pathlib import Path
import subprocess
from typing import Dict, List
from xdg import DesktopEntry
from linkwiz.config import config

SELF_DESKTOP: str = "linkwiz.desktop"
HTTP_HANDLER: str = "x-scheme-handler/http"

DESKTOP_PATHS = [
    Path("/usr/share/applications/"),
    Path.home() / ".local/share/applications/",
]

MIMEINFO_PATHS = [
    Path("/usr/share/applications/mimeinfo.cache"),
    Path.home() / ".local/share/applications/mimeinfo.cache",
]


def get_browsers() -> Dict[str, Path]:
    """Get the name and exec path of browsers."""
    try:
        installed_browsers = []
        if config.main.get("auto_find_browsers", True):
            installed_browsers = find_installed_browsers()

        browsers = get_browser_exec(installed_browsers)
        browsers.update(config.browsers)

        return browsers
    except subprocess.CalledProcessError:
        logging.error("Error getting installed browsers")
        exit(1)


def find_installed_browsers() -> List[str]:
    """Get the name of installed browsers."""
    installed_browsers = set()
    for path in MIMEINFO_PATHS:
        if not path.exists():
            continue
        with open(path, "r") as f:
            for line in f:
                if not line.startswith(HTTP_HANDLER):
                    continue
                browsers = line.split("=")[-1].strip().split(";")
                installed_browsers.update(browsers)
                break
    installed_browsers.discard(SELF_DESKTOP)
    return list(installed_browsers)


def get_browser_exec(browsers_desktop: List[str]) -> Dict[str, Path]:
    """Get the exec path of installed browsers."""
    browsers_exec: Dict[str, Path] = {}
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
