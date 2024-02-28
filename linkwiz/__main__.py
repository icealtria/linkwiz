import sys
from linkwiz.core import process_url


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
        process_url(arg)


if __name__ == "__main__":
    main()
