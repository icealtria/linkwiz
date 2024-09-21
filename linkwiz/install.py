import platform


from linkwiz.installation.linux_install import (
    install_app_in_linux,
    uninstall_app_in_linux,
)
from linkwiz.installation.win_install import (
    install_app_in_windows,
    unregister_app_in_windows,
)


def install(script_path: str):
    if platform.system() == "Linux":
        install_app_in_linux(script_path)
    elif platform.system() == "Windows":
        install_app_in_windows(script_path)
    print("Installed")


def uninstall():
    if platform.system() == "Linux":
        uninstall_app_in_linux()
    elif platform.system() == "Windows":
        unregister_app_in_windows()
        print("Uninstalled")
