def write(ax, output_dir, name):
    try:
        if name.split(".")[-1] != "html":
            ax.write_image(f"{output_dir}/{name}")

        else:
            ax.write_html(f"{output_dir}/{name}")
    except PermissionError:
        print(f"Not allowed to write to {output_dir}")

