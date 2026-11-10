def write(text, output, name):
    """
    Writes a CAMI profile to disk
    :param text: String containing text that should be written
    :param output: String containing output directory
    :param name: String containing the name of the file
    :return: None if permission error is raised
    """
    try:
        with open(f"{output}/{name}", "w", encoding="utf-8") as f:
            f.write(text)
    except PermissionError as _:
        print("No permission to write at {output}")
        return None
