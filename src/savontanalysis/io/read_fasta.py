import gzip
def main(fasta_path):
    try:
        if fasta_path.endswith(".gz"):
            with gzip.open(fasta_path, "r") as f:
                fasta = f.read()
        else:
            with open(fasta_path, "r") as f:
                fasta = f.read()
    except FileNotFoundError as _:
        print("abundance file not found, did you give the right input directory?")
        return None
    print(fasta)
    return fasta
