import logging
from typing import Optional
from linkwiz.config import custom_rules
from linkwiz.open import open_link
import re

logger = logging.getLogger(__name__)


def get_browser_for_url(url) -> Optional[str]:
    for pattern, browser in custom_rules.items():
        if re.match(pattern, url):
            logger.info(f"Matched {url} to {browser}")
            return browser
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
