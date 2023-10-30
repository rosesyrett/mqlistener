import subprocess
import sys

from mqlistener import __version__


def test_cli_version():
    cmd = [sys.executable, "-m", "mqlistener", "--version"]
    assert subprocess.check_output(cmd).decode().strip() == __version__
