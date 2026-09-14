def write(ax, output_dir, name):
    try:
        ax.write_image(f"{output_dir}/{name}")
    except PermissionError:
        print(f"Not allowed to write to {output_dir}")