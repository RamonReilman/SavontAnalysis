import pandas as pd

def main(input_dir):
    try:
        data = pd.read_csv(f"{input_dir}/species_abundance.tsv", delimiter = "\t")
    except FileNotFoundError as e:
        print("Species abundance file not found, did you give the right input directory?")
        return None
    except NotADirectoryError as e:
        print(f"Input directory: {input_dir}, is not a directory")
        return None

    return data
