from pathlib import Path

def main(path):
    path = Path(path)
    try:
        path.mkdir(parents=True, exist_ok=True)
    except PermissionError as _:
        print("Directory could not be made (check permissions)")
        return False