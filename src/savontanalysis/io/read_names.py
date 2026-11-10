import pandas as pd


def main(names_path):
    """
    Read names file
    :param names_path: String containing path to names
    :return: DF of names file
    """
    df = pd.read_csv(
        names_path,
        sep="\t\|\t",
        engine="python",
        header=None,
        names=["id", "name", "classification", "type", "_"],
        dtype="string",
    )

    df = df.drop(columns="_")
    df = df.apply(lambda col: col.str.strip())
    df = df.replace("", pd.NA)

    return df

