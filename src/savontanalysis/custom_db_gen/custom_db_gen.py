# TODO split things up into smaller functions
# TODO put the writing of files into IO functions
from typing import Any, Callable
from savontanalysis.taxonomy.database import TaxonomyDB
from savontanalysis.io import dir_check, read_tab_pandas


def register(subparser):
    p = subparser.add_parser("customdb",
                             help="Generates a custom db for wf-16s")
    p.add_argument("--db_type",
                   help="Specify the type of db input",
                   choices=["silva", "greengenes2"],
                   required=True)
    p.add_argument("--input_fasta", required=True)
    p.add_argument("--tax_file", help="tax_slv_lsu file belonging to Silva, used to get better rank assignment")
    p.add_argument("--output_dir", default="./")
    p.add_argument("--db_path", required = True, help="Location where db will be saved")


def run(args):
    """
    Generates the following files needed for wf-16s:
    ref2taxid.tsv: headerID of ref db with custom taxIDS
    nodes.dmp: Information about the taxids
    names.dmp Links the name of a taxon with a taxid
    :param args: CLI arguments
    :return: -
    """
    cache = {}

    if dir_check.main(args.output_dir) is False:
        return None
    rank_lookup = None
    if args.tax_file is not None:
        tax_file = read_tab_pandas.main(args.tax_file, header=None).dropna(axis = 1, how = "all")
        print(tax_file)
        tax_file.columns = ["lineage", "taxid", "rank", "version"]

        rank_lookup = dict(zip(tax_file["lineage"], tax_file["rank"]))


    if args.db_type == "greengenes2":
        taxmap = {
            "d__": "superkingdom",
            "p__": "phylum",
            "c__": "class",
            "o__": "order",
            "f__": "family",
            "g__": "genus",
            "s__": "species"
        }
    db = TaxonomyDB(args.db_path)

    rows = []
    ref2tax = {}

    db.add_taxon(1, "root", "no rank")
    rows_db = db.get_all()
    for taxid, parent_id, name, rank in rows_db:
        key = (name, rank, parent_id)
        cache[key] = taxid

    def get_or_create(parent_id, name, rank):

        key = (name, rank, parent_id)
        if key in cache:
            return cache[key]
        taxid = db.add_taxon(parent_id, name, rank)
        cache[key] = taxid
        return taxid

    seq_id = 0
    with open(str(args.input_fasta), "r") as f:
        for line in f:
            if line.startswith(">"):
                if args.db_type == "greengenes2":
                    parentID = greengenes2_processing(get_or_create, line, taxmap)
                    ref2tax[f"gg{seq_id}"] = parentID if parentID is not None else 0
                    line = f">gg{seq_id} {line[1:]}"
                elif args.db_type == "silva":
                    parentID, accession = silva_processing(get_or_create, line, rank_lookup)
                    ref2tax[accession] = parentID if parentID is not None else 0

                seq_id += 1
            rows.append(line)

    write_gg2(args, rows)

    write_ref2taxic(args, ref2tax)

    writing_names_nodes(args, db)


def writing_names_nodes(args, db):
    rows = db.get_all()
    valid_ranks = ["domain", "phylum", "class", "order", "family", "genus", "species"]
    with open(f"{args.output_dir}/names.dmp", "w") as names, \
            open(f"{args.output_dir}/nodes.dmp", "w") as nodes:
        names.write("1\t|\troot\t|\t\t|\tscientific name\t|\n")
        nodes.write("1\t|\t1\t|\tno rank\t|\t\t|\t0\t|\t1\t|\t11\t|\t1\t|\t0\t|\t1\t|\t0\t|\t0\t|\t\t|\n")
        for row in rows[1:]:
            id = row[0]
            parent_id = row[1]
            name = row[2]
            rank = row[3]

            if rank not in valid_ranks:
                rank = "no rank"
            if rank == "domain":
                rank = "superkingdom"

            if parent_id is None:
                parent_id = 1

            names.write(f"{id}\t|\t{name}\t|\t\t|\tscientific name\t|\n")
            nodes.write(
                f"{id}\t|\t{parent_id}\t|\t{rank or 'no rank'}\t|\t\t|\t0\t|\t1\t|\t11\t|\t1\t|\t0\t|\t1\t|\t0\t|\t0\t|\t\t|\n")


def write_ref2taxic(args, ref2tax):
    print("writing ref2taxid")
    with open(f"{args.output_dir}/ref2taxid.tsv", "w") as f:
        for key, value in ref2tax.items():
            f.write(f"{key}\t{value}\n")


def write_gg2(args, rows):
    print("writing gg2")
    with open(f"{args.output_dir}/gg2_renamed.fa", "w") as f:
        f.write("".join(rows))


def greengenes2_processing(get_or_create: Callable[..., Any | None], line: str,
                           taxmap: dict[str, str] | dict[int, str]) -> Any:
    header = line[1:].strip().rstrip(";")
    fields = header.split(";")
    lowest_rank = taxmap[fields[-1][0:3]]
    name = fields[-1][3:]
    if lowest_rank == "species":
        name = f"{fields[-2][3:]} {fields[-1][3:]}"

    parentID = None
    for i, field in enumerate(fields):
        rank = taxmap[field[0:3]]
        name = field[3:].strip()
        if rank == "species":
            name = f"{fields[-2][3:].strip()} {field[3:].strip()}".strip()
        if not name:
            break

        parentID = get_or_create(parentID, name, rank)
    return parentID

def silva_processing(get_or_create, line, rank_lookup) -> Any:
    accession, lineage = line[1:].strip().split(" ", 1)
    fields = lineage.split(";")
    # PR2 line
    if "PR2" in accession:
        taxmap = {
            0: "domain",
            1: "supergroup",
            2: "phylum",
            3: "subdivision",
            4: "class",
            5: "order",
            6: "family",
            7: "genus",
            8: "species"
        }


    # Silva structured line
    elif len(fields) == 7:
        taxmap = {
            0: "domain",
            1: "phylum",
            2: "class",
            3: "order",
            4: "family",
            5: "genus",
            6: "species",
        }
    # If uncertain pick safest option
    else:
        taxmap = {0: "domain",
              len(fields)-1: "species",
              len(fields)-2: "genus"}

    parentID = None
    temp_lineage = []
    for i, field in enumerate(fields):
        if rank_lookup is None:
            rank = get_rank_custom(i, taxmap)
        else:
            rank = get_rank_tax_file(field, fields, i, rank_lookup, temp_lineage, taxmap)

        name = field.strip()
        if not name:
            continue
        parentID = get_or_create(parentID, name, rank)

    return parentID, accession


def get_rank_tax_file(field, fields, i: int, rank_lookup, temp_lineage, taxmap) -> str:
    if i == len(fields) - 1:
        return "species"
    temp_lineage.append(f"{field};")
    rank = rank_lookup.get("".join(temp_lineage))
    if rank is None:
        rank = get_rank_custom(i, taxmap)
    return rank


def get_rank_custom(i: int, taxmap: dict[int, str]) -> str:
    if i not in taxmap.keys():
        rank = "no rank"
    else:
        rank = taxmap[i]
    return rank
