from savontanalysis.analysis import savont_abundance_calc
from savontanalysis.io import read_tab_pandas
from savontanalysis.result_merging import tie_breaking_system
import pandas as pd
def register(subparsers):
    p = subparsers.add_parser("savont_result_merger", help="Merge the results of 2 savont runs (same ASV-base)")
    p.add_argument("--asv_directory", required=True)
    p.add_argument("--classify_directories", nargs="+", help = "List of savont classify directories", required = True)

def run(args):
    print("DEBUGGING< LIST SAVONT_ABUNDANCE_CALC LIST == INDEXED BY 0")
    asv_mappings = []
    if len(args.classify_directories) > 0:
        for classify_dir in args.classify_directories:
            asv_mappings.append(read_tab_pandas.main(f"{classify_dir}/asv_mappings.tsv"))

    asv_mapping = pd.concat(asv_mappings)

    feature_table = read_tab_pandas.main(f"{args.asv_directory}/feature-table.tsv")
    asv_mapping = asv_mapping.fillna("")
    create_lineage(asv_mapping)
    final_assignments = read_tab_pandas.main(f"{args.asv_directory}/final_assignments.tsv")

    resolved_lineages = tie_breaking_system.main(asv_mapping)
    clean_lineages_list = clean_lineages(resolved_lineages)
    lineage_abundancies = savont_abundance_calc.main(resolved_lineages, final_assignments, feature_table)
    df = pd.Series(clean_lineages_list).str.split(";", expand = True)
    df.columns = ["species", "genus", "family", "order", "class", "phylum", "clade", "superkingdom"]
    for sample in lineage_abundancies.keys():
        col = []
        for lineage in clean_lineages_list:

            abundance = round(lineage_abundancies[sample][lineage], 6)
            col.append(abundance)

        df[sample] = pd.Series(col)
    print(resolved_lineages)
    df = df.sort_values(by=df.columns[-1], ascending=False)
    print(df)
    df.to_csv("./testoutput.tsv", sep="\t", index=False)

def create_lineage(df):
    cols = ["species", "genus", "family", "order", "class", "phylum",
       "clade", "superkingdom"]
    df["lineage"] = df[cols].apply(lambda row: ";".join(row.values.astype(str)), axis = 1)

def clean_lineages(resolved_lineages):
    cleaned_lineages = []
    for lineage in resolved_lineages.values():
        if lineage not in cleaned_lineages:
            cleaned_lineages.append(lineage)
    return cleaned_lineages