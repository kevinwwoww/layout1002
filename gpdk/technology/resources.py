from pathlib import Path


class RESOURCE:
    ROOT_FOLDER = Path(__file__).parent.parent.parent


if __name__ == "__main__":
    print(RESOURCE.ROOT_FOLDER)
