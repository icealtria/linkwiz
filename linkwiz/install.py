from xdg import DesktopEntry, BaseDirectory
from pathlib import Path
import subprocess
import shlex

DESKTOP_FILENAME = "linkwiz.desktop"
DESKTOP_PATH = Path(BaseDirectory.xdg_data_home) / "applications" / DESKTOP_FILENAME


def install(script_path: str):
    create_linkwiz_desktop_entry(script_path)
    mime_types = ["x-scheme-handler/http", "x-scheme-handler/https"]
    for mime_type in mime_types:
        set_default_app_for_mime_type(mime_type)
    print("Installed")


def create_linkwiz_desktop_entry(script_path: str):
    desktop = DesktopEntry.DesktopEntry(DESKTOP_PATH)
    desktop.set("Name", "Linkwiz")
    desktop.set("Type", "Application")
    desktop.set("MimeType", "x-scheme-handler/http;x-scheme-handler/https;")
    desktop.set("Categories", "Network;")
    desktop.set("NoDisplay", "true")
    desktop.set("Exec", script_path + " %u")
    desktop.write()


def set_default_app_for_mime_type(mime_type: str):
    cmd = ["xdg-mime", "default", DESKTOP_FILENAME, mime_type]
    mime_type_quoted = shlex.quote(mime_type)
    subprocess.run(cmd + [mime_type_quoted], check=True)


def uninstall():
    if DESKTOP_PATH.exists():
        DESKTOP_PATH.unlink()
        print("Uninstalled")
    else:
        print("linkwiz is not installed.")
