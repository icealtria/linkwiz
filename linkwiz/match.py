from typing import Optional
from linkwiz.config import custom_rules
from linkwiz.browser import get_installed_browsers
from linkwiz.open import open_link
import re


def get_browser_for_url(url) -> Optional[str]:
    for pattern, browser in custom_rules.items():
        print(pattern, browser)
        if re.match(pattern, url):
            return browser
    return None

def match_url(browsers, url):
    browser = get_browser_for_url(url)
    for name, path in browsers.items():
        if browser == name:
            open_link(path, url)
            exit()