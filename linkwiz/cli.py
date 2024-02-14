import sys
from urllib.parse import urlparse
from .mimeapps import get_installed_browsers, open_link


def print_installed_browsers(browsers):
    """Prints the list of installed browsers."""
    print("Select a browser:")
    for i, browser_name in enumerate(browsers.keys()):
        print(f"{i+1}. {browser_name}")


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
            browsers = get_installed_browsers()
            print_installed_browsers(browsers)
            choice = input("Enter the number of the browser to use: ")
            try:
                choice_index = int(choice) - 1
                selected_browser = list(browsers.values())[choice_index]
                open_link(selected_browser, arg)
            except (ValueError, IndexError):
                print("Invalid choice.")
        else:
            print("Invalid URL.")
