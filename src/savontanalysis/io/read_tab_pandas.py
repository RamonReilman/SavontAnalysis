import pandas as pd

def main(mapping_path):
    print(mapping_path)
    try:
        data = pd.read_csv(mapping_path, delimiter = "\t")
    except FileNotFoundError as _:
        print("abundance file not found, did you give the right input directory?")
        return None

    return data