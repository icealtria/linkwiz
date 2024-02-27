import logging
from typing import Optional
from linkwiz.config import rules_hostname, rules_regex
from linkwiz.open import open_link
import fnmatch
import re

logger = logging.getLogger(__name__)


def get_browser_for_url(url) -> Optional[str]:
    try:
        for pattern, browser in rules_hostname.items():
            if fnmatch.fnmatch(pattern, url):
                logger.info(f"Matched {url} to {browser}")
                return browser
        for regex, browser in rules_regex.items():
            if re.match(regex, url):
                logger.info(f"Matched {url} to {browser}")
                return browser
    except Exception as e:
        logger.error(f"Error matching {url} to {pattern}: {e}")
    return


def match_url(browsers, url):
    browser = get_browser_for_url(url)
    if browser is None:
        logger.info(f"No match for {url}")
        return
    for name, path in browsers.items():
        if browser == name:
            logger.info(f"Opening {url} with {name}")
            open_link(path, url)
