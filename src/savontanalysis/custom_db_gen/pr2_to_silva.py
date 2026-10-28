from savontanalysis.io import dir_check, read_fasta, read_pr2_merged
from savontanalysis.db_merging.db_merge import get_taxmap_info
import pandas as pd
def register(subparser):
    p = subparser.add_parser("PR2Transform", help="Transform PR2 database into Silva format")
    p.add_argument("--pr2_fasta", required = True, help = "PR2 fasta file")
    p.add_argument("--pr2_information", required = True, help = "PR2 .xlsx file (excel file containing pr2_accession and taxo_id)")
    p.add_argument("--output_dir", default="./")

def run(args):
    if dir_check.main(args.output_dir) is False:
        return
    pr2_fasta = read_fasta.main(args.pr2_fasta)
    pr2_information = read_pr2_merged.main(args.pr2_information)

    if pr2_fasta is None or pr2_information is None:
        return

    fasta_data, tax_map = process_fasta(pr2_fasta, pr2_information)
    taxmap = pd.DataFrame(tax_map, columns=["primaryAccession", "start", "stop", "path", "organism_name", "taxid"])

    taxmap.to_csv(f"{args.output_dir}taxmap.txt", sep="\t", index=False)

    with open(f"{args.output_dir}/merged_db.fasta", "w") as f:
        for line in fasta_data:
            f.write(line)



def process_fasta(fasta, information):
    tax_map = []
    fasta_data = []
    invalid_indices = [1,2,3, 5, 6]

    # Not used but to highlight the keys
    tax_map_info = {"accession": "",
                    "tax_id": "",
                    "start": 0,
                    "end": 0,
                    "taxonomy_path": "",
                    "species": ""}

    info_lookup = information.set_index("pr2_accession")
    for line in fasta:
        if line.startswith(">"):
            tax_map_info = {}
            line = line.replace("_", " ").strip().split("|")
            filtered_header = [item for index, item in enumerate(line) if index not in invalid_indices]
            header = ";".join(filtered_header).replace(";", " ", 1).replace(" ", "_", 1)
            accession = line[0][1:].replace(" ", "_")

            get_taxmap_info(accession, filtered_header, info_lookup, tax_map_info)
            tax_map.append([tax_map_info["accession"], tax_map_info["start"], tax_map_info["end"],
                            tax_map_info["taxonomy_path"], tax_map_info["species"], tax_map_info["tax_id"]])
            fasta_data.append(f"{header}\n")
        else:
            fasta_data.append(line)
    return fasta_data, tax_map



