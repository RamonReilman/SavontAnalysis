import gzip
def main(fasta_path):
    try:
        if fasta_path.endswith(".gz"):
            with gzip.open(fasta_path, "rt") as f:
                fasta = f.readlines()
        else:
            with open(fasta_path, "r") as f:
                fasta = f.readlines()
    except FileNotFoundError as _:
        print("abundance file not found, did you give the right input directory?")
        return None
    return fasta
