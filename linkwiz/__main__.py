import sys
from urllib.parse import urlparse
from linkwiz.app import LinkwizApp


def main():
    """Entry point of the program."""
    if len(sys.argv) != 2:
        print("Usage: python main.py [install | uninstall | url]")
        return

    arg = sys.argv[1]

    if arg == "install":
        print("Installing...")
    elif arg == "uninstall":
        print("Uninstalling...")
    else:
        url_components = urlparse(arg)
        if url_components.scheme in ["http", "https"]:
            app = LinkwizApp(arg)
            app.run()
        else:
            print("Invalid URL.")


if __name__ == "__main__":
    main()
