from savontanalysis.analysis import savont_abundance_calc
from savontanalysis.io import read_tab_pandas
def register(subparsers):
    p = subparsers.add_parser("savont_result_merger", help="Merge the results of 2 savont runs (same ASV-base)")
    p.add_argument("--asv_directory", required=True)
    p.add_argument("--classify_directories", nargs="+", help = "List of savont classify directories", required = True)

def run(args):
    print("DEBUGGING< LIST SAVONT_ABUNDANCE_CALC LIST == INDEXED BY 0")
    classify_dir = args.classify_directories[0]
    asv_mapping = read_tab_pandas.main(f"{classify_dir}/asv_mappings.tsv")
    final_assignments = read_tab_pandas.main(f"{args.asv_directory}/final_assignments.tsv")
    lineage_abundancies = savont_abundance_calc.main(asv_mapping, final_assignments)
    print(lineage_abundancies)