import platform
import sys
from linkwiz.install import install, uninstall


def main():
    """Entry point of the program."""

    if platform.system() != "Linux" and platform.system() != "Windows":
        print("Platform not supported")
        return

    if len(sys.argv) != 2:
        print("Usage: linkwiz [install | uninstall | <url>]")
        return

    arg = sys.argv[1]

    if arg == "install":
        install(sys.argv[0])
    elif arg == "uninstall":
        uninstall()
    else:
        from linkwiz.core import process_url

        process_url(arg)


if __name__ == "__main__":
    main()
