import subprocess
import sys
from pathlib import Path
from time import perf_counter


def test_examples():
    CT_Cu_pdk_folder = Path(__file__).parent
    examples_folder = CT_Cu_pdk_folder / "examples"
    pyfiles = tuple(examples_folder.glob("example_*.py"))
    total = len(pyfiles)
    start_at = perf_counter()
    for i, pyfile in enumerate(pyfiles):
        print(f"Running {pyfile} ... {i+1}/{total}")
        subprocess.run([sys.executable, pyfile], check=True)
    end_at = perf_counter()
    print(f"Complete in {end_at - start_at} seconds.")


if __name__ == "__main__":
    test_examples()
