import pandas as pd

def main(input_dir):
    """
    Reads the abundance table of wf-16s workflow output
    :param input_dir: The dir that stores the wf-16s output
    :return: Pandas dataframe containing the abundance table data.
    """
    try:
        data = pd.read_csv(f"{input_dir}/abundance_table_genus.tsv", delimiter = "\t")
    except FileNotFoundError as e:
        print("abundance file not found, did you give the right input directory?")
        return None
    except NotADirectoryError as e:
        print(f"Input directory: {input_dir}, is not a directory")
        return None

    return data
