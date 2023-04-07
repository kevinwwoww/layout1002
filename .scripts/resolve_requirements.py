import os
import subprocess
import sys

from config import NETWORK_ACCESS, PIP_PACKAGE_FOLDERS, PIP_INDEX_URL, PIP_TRUSTED_HOST

if __name__ == "__main__":
    venv_folder = os.environ.get("VIRTUAL_ENV")
    if venv_folder is None:
        print("Please create virtual environment first")
        exit(1)

    subprocess.run(
        [sys.executable, "-m", "pip", "config", "--site", "set", "install.find-links", " ".join(it.absolute().as_uri() for it in PIP_PACKAGE_FOLDERS)], check=True
    )
    subprocess.run([sys.executable, "-m", "pip", "config", "--site", "set", "global.index-url", PIP_INDEX_URL], check=True)
    subprocess.run([sys.executable, "-m", "pip", "config", "--site", "set", "global.trusted-host", PIP_TRUSTED_HOST], check=True)
    subprocess.run([sys.executable, "-m", "pip", "config", "--site", "set", "install.no-index", "false" if NETWORK_ACCESS else "true"], check=True)

    subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], check=True)
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
