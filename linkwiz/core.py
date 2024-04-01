from urllib.parse import urlparse
import logging

from linkwiz.browser import get_browsers
from linkwiz.match import find_matching_browser
from linkwiz.gui import LinkwizGUI
from linkwiz.launch import launch_browser
from linkwiz.config import config


def process_url(url):
    """Process the provided URL."""
    parsed_url = urlparse(url)

    if parsed_url.scheme not in ("http", "https"):
        raise ValueError("Invalid URL.")

    if config.features.get("remove_track", False):
        url = remove_tracking(url)
    browsers = get_browsers()

    try:
        launch_browser_command = find_matching_browser(
            browsers, parsed_url.geturl(), parsed_url.netloc
        )
        if launch_browser_command:
            launch_browser(*launch_browser_command)
            return

        app = LinkwizGUI(browsers, url)
        launch_browser_command = app.run()
        launch_browser(*launch_browser_command)

    except Exception as e:
        logging.error(f"Error processing URL: {e}")


def remove_tracking(url):
    """Remove tracking parameters from the URL."""
    try:
        import unalix
        return unalix.clear_url(url=url)
    except ImportError:
        logging.warning("The 'unalix' package is not installed. Cannot remove tracking parameters.")
        return url