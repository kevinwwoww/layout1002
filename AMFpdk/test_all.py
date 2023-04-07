import os
import subprocess


def run_tests():
    subprocess.run(
        [
            "pytest",
            "--new-first",
            "-o",
            "python_files=test_*.py",
            "-o",
            "python_functions=test_*",
            os.path.dirname(__file__),
        ],
    )


if __name__ == "__main__":
    run_tests()
