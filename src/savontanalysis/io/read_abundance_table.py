import pandas as pd
import glob


def main(input_dir):
    """
    Reads the abundance table of wf-16s workflow output
    :param input_dir: The dir that stores the wf-16s output
    :return: Pandas dataframe containing the abundance table data.
    """
    file = glob.glob(f"{input_dir}/*abundance_table_*.tsv")
    if not file:
        raise FileNotFoundError(
            f"No '*abundance_table_*.tsv' file found in {input_dir}"
        )
    data = pd.read_csv(file[0], delimiter="\t")

    return data
