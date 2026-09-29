import pandas as pd
from pandas import DataFrame
import glob
from savontanalysis.io import read_species_abundance, write_profile, read_abundance_table, read_nanosim_ab
import re
from savontanalysis.taxonomy.database import TaxonomyDB

def register(subparser):
    p = subparser.add_parser("profile2CAMI", help="Generates a names2taxid file using taxonkit")
    p.add_argument("--input_dir", required=True)
    p.add_argument("--output_dir", default="./")
    p.add_argument("--tool", help = "tool used to generate file", required = True, choices = ["savont", "wf-16s", "nanosim"])
    p.add_argument("--sampleID", help = "Name the sampleID in the header", required = True)



def run(args):
    db = TaxonomyDB("~/.local/share/tax.db")
    if args.tool == "savont":
        species_abundance = read_species_abundance.main(args.input_dir)
        print(species_abundance)
        if species_abundance is None:
            return
        build_output_savont(args, db, species_abundance)
    elif args.tool == "wf-16s":
        species_abundance = read_abundance_table.main(args.input_dir)
        if species_abundance is None:
            return
        build_output_wf16s(args, db, species_abundance)
    else:
        new_df = {"percentage": [],}
        abundance = read_nanosim_ab.main(args.input_dir)
        for row in abundance.itertuples(index = False):
            tax_id = row[0]
            abundance = row[1]
            new_df["percentage"].append(abundance / 100)
            taxon = db.fetch_with_id(tax_id)
            parent_id = taxon[1]

            while parent_id is not None:
                if taxon[3] not in new_df:
                    new_df[taxon[3]] = []

                new_df[taxon[3]].append(taxon[2])

                taxon = db.fetch_with_id(parent_id)
                parent_id = taxon[1]
            if taxon[3] not in new_df:
                new_df[taxon[3]] = []
            new_df[taxon[3]].append(taxon[2])

        ground_truth_abundances = pd.DataFrame(new_df)
        colnames = ground_truth_abundances.columns.to_list()
        body = build_body(colnames[1:], ground_truth_abundances, "percentage", db)
        header = build_header(args.sampleID, reversed(colnames[1:]))
        write_profile.write(header + body, args.output_dir, f"ground_truth.profile")





def build_output_wf16s(args, db, species_abundance):
    ranks = ["superkingdom", "clade", "phylum", "class", "order", "family", "genus", "species"]
    n_ranks = len(species_abundance["tax"].str.split(";")[0])
    ranks = ranks[0:n_ranks]

    species_abundance[ranks] = species_abundance["tax"].str.split(";", expand=True)
    counts = species_abundance.iloc[:, 1]
    species_abundance["percentage"] = counts / counts.sum()
    species_abundance.drop(["tax", "clade", "total"], inplace=True, axis=1)
    print(species_abundance)
    header = build_header(args.sampleID, ranks)
    ranks.pop(ranks.index("clade"))
    ranks.reverse()
    body = build_body(ranks, species_abundance, "percentage", db)
    write_profile.write(header + body, args.output_dir, f"wf-16s.profile")


def build_output_savont(args, db: TaxonomyDB, species_abundance: DataFrame):
    print(species_abundance)
    if "clade" in species_abundance.columns:
        species_abundance.drop(['clade'], inplace=True, axis=1)

    col_names = list(species_abundance.columns)
    final_col = col_names.index("superkingdom")
    if "abundance" in col_names:
        sample_list = ["abundance"]
        _ = col_names.pop(0)
    else:

        print(col_names)
        sample_list = col_names[final_col + 1::]

    for i in range(0, len(sample_list)):
        header = build_header(args.sampleID, reversed(col_names[0:final_col+1]))
        body = build_body(col_names[0:final_col + 1], species_abundance, sample_list[i], db)
        write_profile.write(header + body, args.output_dir, f"{sample_list[i]}.profile")


def build_body(colnames, data, percentage_col, db):
    EMITS = ["Greengenes_unannotated", "UNCLASSIFIED", "Unknown", "Unclassified"]
    body = ""
    ranks = list(reversed(colnames))
    for rank_i, rank in enumerate(ranks):
        if rank_i == 0:
            groups = data[[rank]].drop_duplicates().itertuples(index = False)
            parent_rank = None
        else:
            parent_rank = ranks[rank_i-1]
            groups = data[[parent_rank, rank]].drop_duplicates().itertuples(index = False)

        for group in groups:
            if parent_rank is None:
                name, parent = group[0], None
                mask = data[rank] == name
            else:
                parent, name = group
                mask = (data[rank] == name) & (data[parent_rank] == parent)
            percentage = round(data[mask][percentage_col].sum() * 100, 5)

            if name in EMITS:
                continue
            id = db.get_taxID(name, rank)
            if id is None:
                id = db.add_taxon(None, name, rank)
            parentID = db.get_taxID(parent, parent_rank)
            db.update_parentID(parentID, name, rank)

            taxpath = [id]
            taxpathsn = [name]

            while parentID is not None:
                taxpath.append(parentID)

                parent_info = db.fetch_with_id(parentID)
                taxpathsn.append(parent_info[2])
                parentID = parent_info[1]
            taxpath.reverse()

            taxpathsn.reverse()
            sep = "|"
            temp_body = f"{id}\t{rank}\t{sep.join(map(str,taxpath))}\t{sep.join(map(str,taxpathsn))}\t{percentage}\n"
            body += temp_body

    return body


def build_header(sampleID, ranks):
    header = f"""# Taxonomic profiling output
@SampleID:{sampleID}
@Version:0.9.3
@TaxonomyID:greengenes2-2024.09
@Ranks:{"|".join(ranks)}
@@TAXID	RANK	TAXPATH	TAXPATHSN	PERCENTAGE
"""
    return header