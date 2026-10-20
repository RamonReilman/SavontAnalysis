import pandas as pd
def main(taxmap_path):
    try:
        tax_map = pd.read_csv(taxmap_path,header = 0, sep="\t")
        return tax_map
    except FileNotFoundError as _:
        print("tax map not found, did you give the right input file?")
        return None