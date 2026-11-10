import gzip


def main(fasta_path):
    """
    Reads a fasta file, can be a .gz file
    :param fasta_path: String of where the fasta file is located
    :return: List of strings containing the contents of the file.
    None if it could not be read
    """
    try:
        if fasta_path.endswith(".gz"):
            with gzip.open(fasta_path, "rt") as f:
                fasta = f.readlines()
        else:
            with open(fasta_path, "r") as f:
                fasta = f.readlines()
    except FileNotFoundError as _:
        print("abundance file not found, "
              "did you give the right input directory?")
        return None
    return fasta
