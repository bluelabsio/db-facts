from typing import List, Union
import subprocess


def backtick(cmd: Union[str, List[str]]) -> str:
    return subprocess.check_output(cmd).decode('utf-8').strip()
