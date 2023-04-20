from pathlib import Path


def local_output_file(src_file: str) -> Path:
    return Path(src_file).parent / "local" / Path(src_file).with_suffix(".gds").name
