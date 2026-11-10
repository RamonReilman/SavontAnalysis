from pathlib import Path


def main(path):
    """
    Checks if path is a dir \n
    If dir does not exist, create it
    :param path: string of path to be checked
    :return: True if exists, false if dir was not created
    """
    path = Path(path)
    if path.suffix:
        return True
    try:
        path.mkdir(parents=True, exist_ok=True,)
        return True
    except PermissionError as _:
        print("Directory could not be made (check permissions)")
        return False
