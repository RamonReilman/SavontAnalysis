from pathlib import Path


def write(ax, output_dir, name):
    """
    Writes a plot to disk
    :param ax: Plot
    :param output_dir: The directory the plot should be written to
    :param name: Name of the file
    :return: None
    """
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    try:
        if name.split(".")[-1] != "html":
            ax.write_image(f"{output_dir}/{name}")

        else:
            ax.write_html(f"{output_dir}/{name}")
    except PermissionError:
        print(f"Not allowed to write to {output_dir}")
