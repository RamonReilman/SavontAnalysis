from savontanalysis.taxonomy.database import TaxonomyDB
from savontanalysis.io import read_fasta
def register(subparser):
    p = subparser.add_parser("mergeDB", help="Merge 2 reference databases into one")
    p.add_argument("--base_db", required=True)
    p.add_argument("--tax_map")
    p.add_argument("--new_db", required = True)
    p.add_argument("--output_dir", default="./")

def run(args):
    try:
        check_supported_dbs(args)
    except Exception as e:
        print(e)
        return None
    fasta = read_fasta.main(args.base_db)
    if fasta is None:
        return None

    for line in fasta:
        print(line)
        break

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
    return 0


