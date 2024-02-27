from pathlib import Path
import subprocess
from typing import List, Union


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
    if isinstance(exe, Path):
        exe_str = exe.as_posix()
    elif isinstance(exe, str):
        exe_str = exe
    else:
        raise TypeError("Executable field must be a string or a Path object.")

    if "%u" not in exe_str and "%U" not in exe_str:
        exe_str = f"{exe_str} {link}"
    return exe_str.replace("%u", link).replace("%U", link).split()


def open_link(exe: Union[Path, str], link: str) -> None:
    """
    Open the link using the specified executable.
    """
    cmd = exec_field_to_cmds(exe, link)
    try:
        subprocess.Popen(
            cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False
        )
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error opening link: {e}")
    exit()
