import pandas as pd

def main(input_dir):
    try:
        data = pd.read_csv(f"{input_dir}/abundance_table_genus.tsv", delimiter = "\t")
    except FileNotFoundError as e:
        print("abundance file not found, did you give the right input directory?")
        return None
    except NotADirectoryError as e:
        print(f"Input directory: {input_dir}, is not a directory")
        return None

    return data
