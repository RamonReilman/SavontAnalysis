import pandas as pd
import glob
def main(input_dir):
    try:
        file = glob.glob(f"{input_dir}/*quantification.tsv")
        abundances = pd.read_csv(file[0], delimiter="\t")
        return abundances
    except IndexError as _:
        print(f"Quantification file could not be found in dir: {input_dir}")
        return None


