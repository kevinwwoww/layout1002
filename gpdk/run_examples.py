import subprocess
import sys
from pathlib import Path
from time import perf_counter
from typing import Any, Mapping, Optional


def run_examples(env: Optional[Mapping[str, Any]] = None):
    gpdk_folder = Path(__file__).parent
    examples_folder = gpdk_folder / "examples"
    pyfiles = tuple(examples_folder.glob("example_*.py"))
    total = len(pyfiles)
    start_at = perf_counter()
    for i, pyfile in enumerate(pyfiles):
        print(f"Running {pyfile} ... {i+1}/{total}")
        subprocess.run([sys.executable, pyfile], check=True, env=env)
    end_at = perf_counter()
    print(f"Complete in {end_at - start_at} seconds.")


if __name__ == "__main__":
    run_examples()
