import sys
from urllib.parse import urlparse
from linkwiz.app import LinkwizApp
from linkwiz.browser import get_installed_browsers
from linkwiz.match import match_url

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
            match_url(browsers, arg)
            app = LinkwizApp(browsers, arg)
            app.run()
        else:
            print("Invalid URL.")


if __name__ == "__main__":
    main()
