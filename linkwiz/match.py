import logging
from pathlib import Path
from typing import Optional
from linkwiz.types import BrowserExecs
from linkwiz.config import config
import fnmatch


def get_browser_for_url(hostname) -> Optional[str]:
    try:
        for pattern, browser in config.rules_fnmatch.items():
            if fnmatch.fnmatch(hostname, pattern):
                logging.info(f"Matched {hostname} to {browser}")
                return browser
        return config.rules_hostname.get(hostname, None)
    except Exception as e:
        logging.warning(f"Error matching {hostname}: {e}")


def find_matching_browser(browsers: BrowserExecs, url, hostname) -> tuple[Path, str]:
    browser = get_browser_for_url(hostname)
    if browser is None:
        logging.info(f"No match for {url}")
        return
    for name, path in browsers.items():
        if browser == name:
            logging.info(f"Opening {url} with {name}")
            return path, url
