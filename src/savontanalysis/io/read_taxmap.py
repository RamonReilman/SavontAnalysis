import pandas as pd


def main(taxmap_path):
    """
    Reads the Silva taxmap file
    :param taxmap_path: String containing the location of the Silva taxmap
    :return: Pandas dataframe containing the contents of the file.
    None if file could not be read
    """
    try:
        tax_map = pd.read_csv(taxmap_path, header=0, sep="\t")
        return tax_map
    except FileNotFoundError as _:
        print("tax map not found, did you give the right input file?")
        return None
