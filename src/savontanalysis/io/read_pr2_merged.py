import pandas as pd
def main(merged_path):
    try:
        merged_file = pd.read_csv(merged_path,header = 0, sep = ",")
        return merged_file
    except FileNotFoundError as _:
        print("merged file not found, did you give the right input file?")
        return None