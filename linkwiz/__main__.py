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
        ex_url = urlparse(arg)
        if ex_url.scheme in ["http", "https"]:
            browsers = get_installed_browsers()
            open_link_with_matched_browser(browsers, ex_url.geturl(), ex_url.hostname)
            app = LinkwizApp(browsers, arg)
            app.run()
        else:
            logging.error("Invalid URL.")


if __name__ == "__main__":
    main()
