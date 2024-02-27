from pathlib import Path
import subprocess
from typing import List, Union
import logging

def exec_field_to_cmds(exe: Union[Path, str], link: str) -> List[str]:
    """
    Convert the executable field to a list of commands.
    >>> exec_field_to_cmds("firefox %u", "https://example.com")
    ['firefox', 'https://example.com']
    >>> exec_field_to_cmds(Path("firefox"), "https://example.com")
    ['firefox', 'https://example.com']
    >>> exec_field_to_cmds("firefox %U", "https://example.com")
    ['firefox', 'https://example.com']
    >>> exec_field_to_cmds("firefox", "https://example.com")
    ['firefox', 'https://example.com']
    """
    assert isinstance(exe, (Path, str)), "exe must be Path or str"
    exe_str = str(exe) if isinstance(exe, Path) else exe

    cmd = exe_str.replace("%u", link).replace("%U", link)
    if link not in cmd:
        cmd += f" {link}"

    return cmd.split()


def launch_browser(exe: Union[Path, str], link: str) -> None:
    """
    Open the link using the specified executable.
    """
    cmd = exec_field_to_cmds(exe, link)
    try:
        subprocess.Popen(
            cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False
        )
        logging.info(f"Opened link: {link}")
    except (FileNotFoundError, PermissionError) as e:
        logging.error(f"Error opening link: {e}")
    exit()
