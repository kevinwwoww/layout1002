import subprocess
import sys
from pathlib import Path
from time import perf_counter
from fnpcell.ansi.term import Color, print_ansi, style  # type: ignore

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("python time.py <python script>")
        sys.exit(0)

    script = Path(sys.argv[1]).resolve()
    if not script.exists():
        print(f"File not found: {script}")
        sys.exit(0)

    if not script.is_file():
        print(f"Invalid file: {script}")
        sys.exit(0)

    print_ansi(style(color=Color.CYAN), f"Running {script}")
    started_at = perf_counter()
    try:
        subprocess.run([sys.executable, str(script), *sys.argv[2:]], check=True)
    finally:
        duration = perf_counter() - started_at
        print_ansi(style(color=Color.GREEN), f"Elapsed time: {duration}")
