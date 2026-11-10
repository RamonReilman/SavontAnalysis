import pandas as pd
import glob


def main(input_dir):
    """
    Reads the NanoSim abundance file from a directory
    :param input_dir: String of directory
    containing the quantification.tsv file
    :return: Pandas dataframe of the file, or None if it could not be opened
    """
    try:
        file = glob.glob(f"{input_dir}/*quantification.tsv")
        abundances = pd.read_csv(file[0], delimiter="\t")
        return abundances
    except IndexError as _:
        print(f"Quantification file could not be found in dir: {input_dir}")
        return None
