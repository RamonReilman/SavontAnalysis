from pathlib import Path
import logging


def main(path):
    """
    Checks if path is a dir \n
    If dir does not exist, create it
    :param path: string of path to be checked
    :raises OSError: If the directory cannot be created
    """
    path = Path(path)
    if path.suffix or path.is_file():
        path = path.parent
    path.mkdir(parents=True, exist_ok=True)
