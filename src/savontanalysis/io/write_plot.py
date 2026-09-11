def write(ax, output_dir, name):
    try:
        ax.figure.savefig(f"{output_dir}/{name}", bbox_inches="tight", pad_inches=0.1)
    except PermissionError:
        print(f"Not allowed to write to {output_dir}")