def write(text, output, name):
    try:
        with open(f"{output}/{name}", "w", encoding="utf-8") as f:
            f.write(text)
    except PermissionError as _:
        print("No permission to write at {output}")
        return None