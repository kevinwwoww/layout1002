import shutil
import sys
from pathlib import Path

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("python rmtree.py <directory>")
        sys.exit(0)

    path = Path(sys.argv[1]).resolve()
    if not path.exists():
        print(f"Path not found: {path}")
        sys.exit(0)

    shutil.rmtree(path, ignore_errors=True)
