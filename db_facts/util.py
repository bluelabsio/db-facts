from typing import List
import subprocess


def backtick(cmd: List[str]) -> str:
    return subprocess.check_output(cmd).decode('utf-8').strip()
