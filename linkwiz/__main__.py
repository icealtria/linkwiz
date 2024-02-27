import sys
from urllib.parse import urlparse
from linkwiz.app import LinkwizApp
from linkwiz.browser import get_installed_browsers
from linkwiz.match import open_link_with_matched_browser
import logging


def main():
    """Entry point of the program."""
    if len(sys.argv) != 2:
        print("Usage: linkwiz [install | uninstall | <url>]")
        return

    arg = sys.argv[1]

    if arg == "install":
        print("Installing...")
    elif arg == "uninstall":
        print("Uninstalling...")
    else:
        url_components = urlparse(arg)
        if url_components.scheme in ["http", "https"]:
            browsers = get_installed_browsers()
            open_link_with_matched_browser(browsers, url_components.geturl(), url_components.hostname)
            app = LinkwizApp(browsers, arg)
            app.run()
        else:
            logging.error("Invalid URL.")


if __name__ == "__main__":
    main()
