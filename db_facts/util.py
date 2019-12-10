import subprocess


def backtick(cmd):
    return subprocess.check_output(cmd).decode('utf-8').strip()
