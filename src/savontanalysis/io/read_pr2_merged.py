import pandas as pd


def main(merged_path):
    """
    Reads the PR2 merged fasta file
    :param merged_path: Path of the location of the file
    :return: Pandas dataframe of the file, None if it could not be read.
    """
    try:
        merged_file = pd.read_csv(merged_path,header=0, sep=",")
        return merged_file
    except FileNotFoundError as _:
        print("merged file not found, did you give the right input file?")
        return None
