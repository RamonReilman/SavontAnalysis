from pathlib import Path
def write(ax, output_dir, name):
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    try:
        if name.split(".")[-1] != "html":
            ax.write_image(f"{output_dir}/{name}")

        else:
            ax.write_html(f"{output_dir}/{name}")
    except PermissionError:
        print(f"Not allowed to write to {output_dir}")

