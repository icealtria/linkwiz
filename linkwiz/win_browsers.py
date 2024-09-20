import os
from pathlib import Path
from typing import Optional
from linkwiz.types import BrowserExecs


def get_windows_browsers() -> BrowserExecs:
    import winreg

    registry_locations = [
        (winreg.HKEY_CURRENT_USER, winreg.KEY_READ),
        (winreg.HKEY_LOCAL_MACHINE, winreg.KEY_READ | winreg.KEY_WOW64_64KEY),
        (winreg.HKEY_LOCAL_MACHINE, winreg.KEY_READ | winreg.KEY_WOW64_32KEY),
    ]

    browsers = {}
    for tree, access in registry_locations:
        browsers.update(get_browsers_from_registry(tree, access))
    return browsers


def get_browsers_from_registry(tree: int, access: int) -> BrowserExecs:
    """Get installed browsers on Windows from the registry."""
    import winreg

    browsers = {}
    try:
        with winreg.OpenKey(
            tree, r"Software\Clients\StartMenuInternet", access=access
        ) as hkey:
            index = 0
            while True:
                try:
                    subkey = winreg.EnumKey(hkey, index)
                    browser_info = get_browser_info(hkey, subkey)
                    if browser_info:
                        browsers.update(browser_info)
                    index += 1
                except WindowsError:
                    break
    except FileNotFoundError:
        pass

    return browsers


def get_browser_info(hkey, subkey: str) -> Optional[BrowserExecs]:
    """Extract browser information from a specific Windows registry location."""
    import winreg

    try:
        display_name = winreg.QueryValue(hkey, subkey) or subkey

        if display_name == "Internet Explorer":
            return None

        cmd = winreg.QueryValue(hkey, f"{subkey}\\shell\\open\\command")
        cmd = cmd.strip('"')

        os.stat(cmd)
        return {display_name: Path(cmd)}
    except (OSError, AttributeError, TypeError, ValueError):
        return None
