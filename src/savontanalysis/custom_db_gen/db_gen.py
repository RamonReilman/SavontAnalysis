from savontanalysis.taxonomy.database import TaxonomyDB

def register(subparser):
    p = subparser.add_parser("customdb", help="Generates a custom db (greengenes2) based on Savont greengenes2")
    p.add_argument("--input_fasta", required=True)
    p.add_argument("--output_dir", default="./")



def run(args):
    cache = {}
    taxmap = {
        "d__": "superkingdom",
        "p__": "phylum",
        "c__": "class",
        "o__": "order",
        "f__": "family",
        "g__": "genus",
        "s__": "species"
    }
    rows = []
    ref2tax = {}
    db = TaxonomyDB("~/.local/share/tax.db")
    rows_db = db.get_all()
    for taxid, parent_id, name, rank in rows_db:
        key = (name, rank)
        cache[key] = taxid
    def get_or_create(parent_id, name, rank):

        key = (name, rank)
        if key in cache:
            return cache[key]
        taxid = db.add_taxon(parent_id, name, rank)
        cache[key] = taxid
        return taxid

    print(args.input_fasta)
    seq_id = 0
    with open(str(args.input_fasta), "r") as f:
        for line in f:
            if line.startswith(">"):
                header = line[1:].strip().rstrip(";")
                fields = header.split(";")
                lowest_rank = taxmap[fields[-1][0:3]]
                name = fields[-1][3:]
                if lowest_rank == "species":
                    name = f"{fields[-2][3:]} {fields[-1][3:]}"

                parentID = None
                for field in fields:
                    rank = taxmap[field[0:3]]
                    name = field[3:]
                    if rank == "species":
                        name = f"{fields[-2][3:]} {field[3:]}"

                    parentID = get_or_create(parentID, name, rank)
                ref2tax[f"gg{seq_id}"] = parentID if parentID is not None else 0
                line = f">gg{seq_id} {line[1:]}"
                seq_id += 1
            rows.append(line)

    print("writing gg2")
    with open("./gg2_renamed.fa", "w") as f:
        f.write("".join(rows))

    print("writing ref2taxid")
    with open("./ref2taxid.tsv", "w") as f:
        for key, value in ref2tax.items():
            f.write(f"{key}\t{value}\n")


    rows = db.get_all()
    with open("names.dmp", "w") as names, \
    open("nodes.dmp", "w") as nodes:
        for row in rows:
            id = row[0]
            parent_id = row[1]
            name = row[2]
            rank = row[3]

            names.write(f"{id}\t|\t{name}\t|\t\t|\tscientific name\t|\n")
            nodes.write(f"{id}\t|\t{parent_id}\t|\t{rank or 'no rank'}\t|\t\t|\t0\t|\t1\t|\t11\t|\t1\t|\t0\t|\t1\t|\t0\t|\t0\t|\t\t|\n")




