import pandas as pd


def main(mapping_path, header=None):
    """
    Reads a tab-seperated file into a pandas Dataframe
    :param mapping_path: The path of the file to be read (tab separated)
    :param header: If, and on what line, the header exists. Default = `None`
    :return: Pandas dataframe containing the file,
    None if it could not be read.
    """
    print(mapping_path)
    try:
        data = pd.read_csv(mapping_path, delimiter="\t", header=header)
    except FileNotFoundError as _:
        print("abundance file not found, "
              "did you give the right input directory?")
        return None

    return data
