from savontanalysis.analysis import savont_abundance_calc
def register(subparsers):
    p = subparsers.add_parser("savont_result_merger", help="Merge the results of 2 savont runs (same ASV-base)")
    p.add_argument("--asv_directory", required=True)
    p.add_argument("--classify_directories", nargs="+", help = "List of savont classify directories", required = True)

def run(args):
    lineage_abundancies = savont_abundance_calc.main(args)