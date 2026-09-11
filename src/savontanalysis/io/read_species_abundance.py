import pandas as pd

def main(input_dir):
    try:
        test = pd.read_csv(f"{input_dir}/species_abundance.tsv", delimiter = "\t")
    except FileNotFoundError as e:
        print("Species abundance file not found, did you give the right input directory?")
        return None

    return test
