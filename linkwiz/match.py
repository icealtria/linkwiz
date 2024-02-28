import logging
from typing import Optional
from linkwiz.config import rules_hostname, rules_regex
import fnmatch
import re


def get_browser_for_url(hostname) -> Optional[str]:
    try:
        for pattern, browser in rules_hostname.items():
            if fnmatch.fnmatch(pattern, hostname):
                logging.info(f"Matched {hostname} to {browser}")
                return browser
        for regex, browser in rules_regex.items():
            if re.match(regex, hostname):
                logging.info(f"Matched {hostname} to {browser}")
                return browser
    except Exception as e:
        logging.warning(f"Error matching {hostname} to {pattern}: {e}")
    return


def find_matching_browser(browsers, url, hostname):
    browser = get_browser_for_url(hostname)
    if browser is None:
        logging.info(f"No match for {url}")
        return
    for name, path in browsers.items():
        if browser == name:
            logging.info(f"Opening {url} with {name}")
            return path, url
