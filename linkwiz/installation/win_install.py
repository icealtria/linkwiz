import subprocess
import winreg as reg
import sys
import ctypes

from linkwiz.types import APP_NAME


PROTOCOLS = ["http", "https"]


def is_admin():
    """Check if the script is running with administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def install_app_in_windows(script_path: str):
    if not is_admin():
        print("Please run this script as an administrator.")
        exit()

    try:
        register_app_in_windows(script_path)
        open_windows_default_apps_settings()
    except Exception as e:
        print(f"Failed to install app: {e}")


def unregister_app_in_windows():
    if not is_admin():
        print("Please run this script as an administrator.")
        exit()

    try:
        safe_delete_key_recursive(reg.HKEY_CLASSES_ROOT, r"Linkwiz")
        safe_delete_key_recursive(reg.HKEY_CURRENT_USER, r"Software\Linkwiz")
        safe_delete_value(
            reg.HKEY_CURRENT_USER, r"Software\RegisteredApplications", "Linkwiz"
        )

    except Exception as e:
        print(f"Failed to unregister app: {e}")


def safe_create_key(hkey, sub_key):
    try:
        reg.CreateKey(hkey, sub_key)
        print(f"Created or opened: {sub_key}")
    except Exception as e:
        print(f"Failed to create key {sub_key}: {e}")


def safe_set_value(hkey, sub_key, value_name, value):
    try:
        with reg.CreateKey(hkey, sub_key) as key:
            reg.SetValueEx(key, value_name, 0, reg.REG_SZ, value)
            print(f"Set value: {value_name} in {sub_key}")
    except Exception as e:
        print(f"Failed to set value {value_name} in {sub_key}: {e}")


def register_app_in_windows(script_path: str):
    command = f'"{script_path}" "%1"'
    created_keys = []  # Keep track of created keys for rollback
    try:
        # 1. Add ProgID to HKEY_CLASSES_ROOT\Linkwiz
        safe_create_key(reg.HKEY_CLASSES_ROOT, APP_NAME)
        created_keys.append((reg.HKEY_CLASSES_ROOT, APP_NAME))  # Track key
        safe_set_value(
            reg.HKEY_CLASSES_ROOT, f"{APP_NAME}\\shell\\open\\command", "", command
        )

        # 2. Add URL Associations to HKEY_CURRENT_USER\Software\Linkwiz\Capabilities
        user_linkwiz_key = r"Software\Linkwiz\Capabilities\URLAssociations"
        safe_create_key(reg.HKEY_CURRENT_USER, user_linkwiz_key)
        created_keys.append((reg.HKEY_CURRENT_USER, user_linkwiz_key))  # Track key
        safe_set_value(reg.HKEY_CURRENT_USER, user_linkwiz_key, "http", "Linkwiz")
        safe_set_value(reg.HKEY_CURRENT_USER, user_linkwiz_key, "https", "Linkwiz")

        # Add other capabilities
        safe_set_value(
            reg.HKEY_CURRENT_USER,
            r"Software\Linkwiz\Capabilities",
            "ApplicationName",
            "Linkwiz",
        )
        safe_set_value(
            reg.HKEY_CURRENT_USER,
            r"Software\Linkwiz\Capabilities",
            "ApplicationDescription",
            "A tool that lets users select their preferred browser for opening links.",
        )

        # Add shell open command for HKEY_CURRENT_USER
        safe_create_key(reg.HKEY_CURRENT_USER, r"Software\Linkwiz\shell\open")
        created_keys.append(
            (reg.HKEY_CURRENT_USER, r"Software\Linkwiz\shell\open")
        )  # Track key
        safe_set_value(
            reg.HKEY_CURRENT_USER,
            r"Software\Linkwiz\shell\open\command",
            "",
            script_path,
        )

        # 3. Register the application in HKEY_CURRENT_USER\Software\RegisteredApplications
        registered_apps_key = r"Software\RegisteredApplications"
        safe_create_key(reg.HKEY_CURRENT_USER, registered_apps_key)
        created_keys.append((reg.HKEY_CURRENT_USER, registered_apps_key))  # Track key
        safe_set_value(
            reg.HKEY_CURRENT_USER,
            registered_apps_key,
            "Linkwiz",
            r"Software\Linkwiz\Capabilities",
        )

    except Exception as e:
        # Rollback created keys on failure
        print(f"Failed to register app: {e}. Rolling back changes.")
        for hkey, sub_key in reversed(created_keys):  # Rollback in reverse order
            safe_delete_key_recursive(hkey, sub_key)
        print("Rollback complete.")


def open_windows_default_apps_settings():
    """
    Open the Windows Settings page for Default Apps where users can set their default app for HTTP/HTTPS.
    """
    subprocess.run(
        ["start", "ms-settings:defaultapps?registeredAppUser=Linkwiz"], shell=True
    )


def safe_delete_value(hkey, sub_key, value_name):
    try:
        with reg.OpenKey(hkey, sub_key, 0, reg.KEY_SET_VALUE) as key:
            reg.DeleteValue(key, value_name)
            print(f"Deleted value: {value_name} from {sub_key}")
    except FileNotFoundError:
        print(f"Value not found: {value_name} in {sub_key}")
    except Exception as e:
        print(f"Failed to delete value {value_name}: {e}")


def safe_delete_key_recursive(hkey, sub_key):
    try:
        with reg.OpenKey(hkey, sub_key, 0, reg.KEY_READ) as key:
            # Get the number of subkeys
            sub_key_count, _, _ = reg.QueryInfoKey(key)
            # Recursively delete all subkeys
            for i in range(sub_key_count):
                subkey_name = reg.EnumKey(key, 0)  # Always delete the first subkey
                safe_delete_key_recursive(hkey, f"{sub_key}\\{subkey_name}")
        # Once all subkeys are deleted, delete the key itself
        reg.DeleteKey(hkey, sub_key)
        print(f"Deleted: {sub_key}")
    except FileNotFoundError:
        print(f"Key not found: {sub_key}")
    except Exception as e:
        print(f"Failed to delete {sub_key}: {e}")
