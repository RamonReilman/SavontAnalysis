from pathlib import Path

def main(path):
    path = Path(path)
    if path.suffix:
        return True
    try:
        path.mkdir(parents=True, exist_ok=True,)
        return True
    except PermissionError as _:
        print("Directory could not be made (check permissions)")
        return False