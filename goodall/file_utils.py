import os


def get_sub_folders(path: str) -> list:
    return [f.path for f in os.scandir(path) if f.is_dir()]


def get_basename(path: str, with_extension: bool = True) -> str:
    filename = os.path.basename(os.path.normpath(path))
    if with_extension:
        return filename
    return os.path.splitext(filename)[0]
