from typing import Any, Callable
import pandas as pd
from pandas import DataFrame

from savontanalysis.io import read_fasta, read_taxmap, read_pr2_merged
def register(subparser):
    p = subparser.add_parser("mergeDB", help="Merge 2 reference databases into one")
    p.add_argument("--base_db", required=True, help = "Silva fast file")
    p.add_argument("--tax_map", required = True, help = "Silva taxmap file")
    p.add_argument("--new_db", required = True, help = "PR2 fasta file")
    p.add_argument("--new_db_merged", required = True, help = "PR2 merged .xlsx file")
    p.add_argument("--output_dir", default="./")

def run(args):
    try:
        check_supported_dbs(args)
    except Exception as e:
        print(e)
        return None

    fasta_base = read_fasta.main(args.base_db)
    if fasta_base is None:
        return None

    taxmap = read_taxmap.main(args.tax_map)
    PR2_information = read_pr2_merged.main(args.new_db_merged)

    headers, sequences = separate_headers_sequences(fasta_base)
    if len(headers) == 0 or len(sequences) == 0:
        return None

    nucleic_type_base = find_nucleic_acid_type(sequences[0])

    fasta_new = read_fasta.main(args.new_db)
    if fasta_new is None:
        return None

    nucleic_type_second = find_nucleic_acid_type(fasta_new[1])

    converter = get_nucleic_converted(nucleic_type_base, nucleic_type_second)

    new_taxmap, sequences, headers = merge_fasta(converter, fasta_new, headers, sequences, PR2_information)
    taxmap = pd.concat([taxmap, new_taxmap])

    write_merged_db(args, headers, sequences, taxmap)


def write_merged_db(args, headers: list[Any], sequences: list[Any], taxmap: DataFrame):
    taxmap.to_csv(f"{args.output_dir}taxmap.txt", sep="\t", index=False)

    with open(f"{args.output_dir}/merged_db.fasta", "w") as f:
        for i in range(0, len(headers)):
            f.write(f"{headers[i]}\n")
            f.write(f"{sequences[i]}\n")


def get_nucleic_converted(nucleic_type_base: str | None, nucleic_type_second: str | None) -> Callable[..., Any]:
    if nucleic_type_base == "rna" and nucleic_type_second == "dna":
        print("Converting new db into rna")
        converter = dna_to_rna
    elif nucleic_type_base == "dna" and nucleic_type_second == "rna":
        print("Converting new db into dna")
        converter = rna_to_dna
    else:
        converter = same_nucleic_type
    return converter


def merge_fasta(converter: Callable[..., Any] | Callable[..., Any] | Callable[..., Any], fasta_new: list[str],
                headers: list[Any], sequences: list[Any], new_db_info):
    valid_indices = [0, 4, 6, 7, 8, 9, 10, 11, 12]
    tax_map = []
    x = 0
    header = ""
    seen = set(sequences)
    tax_map_info = {"accession": "",
                    "tax_id": "",
                    "start": 0,
                    "end": 0,
                    "taxonomy_path": "",
                    "species": ""}
    info_lookup = new_db_info.set_index("pr2_accession")
    for line in fasta_new:
        if line.startswith(">"):
            tax_map_info = {}
            line = line.replace("_", " ").strip().split("|")
            filtered_header = [item for index, item in enumerate(line) if index in valid_indices]
            header = ";".join(filtered_header).replace(";", " ", 1).replace(" ", "_", 1)
            accession = line[0][1:].replace(" ", "_")
            if accession not in info_lookup.index:
                continue
            get_taxmap_info(accession, filtered_header, info_lookup, tax_map_info)

        else:
            sequence = line.strip()
            sequence_right_nucleic_type = converter(sequence)
            if sequence_right_nucleic_type not in seen:
                seen.add(sequence_right_nucleic_type)
                sequences.append(sequence_right_nucleic_type)
                headers.append(header)
                tax_map.append([tax_map_info["accession"], tax_map_info["start"], tax_map_info["end"],
                                tax_map_info["taxonomy_path"], tax_map_info["species"], tax_map_info["tax_id"]])
            else:
                x+=1
    print(f"{x} duplicates found and not merged")
    return pd.DataFrame(tax_map, columns = ["primaryAccession", "start", "stop", "path", "organism_name", "taxid"]), sequences, headers


def get_taxmap_info(accession: str, filtered_header: list[str], info_lookup, tax_map_info: dict[Any, Any]):
    row = info_lookup.loc[accession]
    tax_map_info["tax_id"] = row["taxo_id"].item()
    tax_map_info["start"] = row["start"].item()
    tax_map_info["end"] = row["end"].item()
    tax_map_info["taxonomy_path"] = ";".join(filtered_header[1:-1:]) + ";"
    tax_map_info["species"] = filtered_header[-1]
    tax_map_info["accession"] = accession.split(".")[0]


def dna_to_rna(sequence):
    return sequence.replace("T", "U")

def rna_to_dna(sequence):
    return sequence.replace("U", "T")

def same_nucleic_type(sequence):
    return sequence


def separate_headers_sequences(fasta: list[str]):
    sequences_base = []
    headers_base = []
    temp_seq = []
    x = 0
    for line in fasta:
        if line.startswith(">"):
            if headers_base:
                sequences_base.append("".join(temp_seq))
            headers_base.append(line.strip())
            temp_seq = []
        else:
            temp_seq.append(line.strip())
    if temp_seq:
        sequences_base.append("".join(temp_seq))

    return headers_base, sequences_base


def find_nucleic_acid_type(sequence):
    sequence = sequence.lower()
    if "u" in sequence:
        return "rna"
    elif "t" in sequence:
        return "dna"
    return None


def check_supported_dbs(args):
    valid = True
    supported_db = ["silva", "pr2"]
    for db in supported_db:
        if db in args.base_db.lower() or db in args.new_db.lower():
            valid = True
            break
        else:
            valid = False
    if not valid:
        raise Exception(f"Databases used in this run are not supported: {supported_db}")
    return True


