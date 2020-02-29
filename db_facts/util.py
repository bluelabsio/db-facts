import subprocess


def backtick(cmd: str) -> str:
    return subprocess.check_output(cmd).decode('utf-8').strip()
