import pandas as pd

def main(mapping_path, header = None):
    print(mapping_path)
    try:
        data = pd.read_csv(mapping_path, delimiter = "\t", header = header)
    except FileNotFoundError as _:
        print("abundance file not found, did you give the right input directory?")
        return None

    return data