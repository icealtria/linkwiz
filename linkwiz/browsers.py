from linkwiz.config import config
from linkwiz.types import BrowserExecs


def get_browsers() -> BrowserExecs:
    """Get the name and exec path of browsers."""
    browsers: BrowserExecs = {}
    if config.main.get("auto_find_browsers", True):
        import platform

        if platform.system() == "Linux":
            from linkwiz.linux_browsers import get_browsers as get_linux_browsers

            browsers.update(get_linux_browsers())
        elif platform.system() == "Windows":
            from linkwiz.win_browsers import get_windows_browsers

            browsers.update(get_windows_browsers())
        else:
            raise NotImplementedError(f"Platform {platform.system()} not supported")

    browsers.update(config.browsers)

    return browsers
