
from savontanalysis.io import read_species_abundance, read_names
import re

def register(subparser):
    p = subparser.add_parser("profile2CAMI", help="Generates a names2taxid file using taxonkit")
    p.add_argument("--input_dir", required=True)
    p.add_argument("--output_dir", default="./")
    p.add_argument("--tool", help = "tool used to generate file", required = True, choices = ["savont", "wf-16s"])
    p.add_argument("--sampleID", help = "Name the sampleID in the header", required = True)
    p.add_argument("--names", help = "taxdump names.dmp file", required = True)



def run(args):
    species_abundance = read_species_abundance.main(args.input_dir)
    if species_abundance is None:
        return
    species_abundance.drop("clade", inplace=True)
    #print(species_abundance)
    map = read_names.main(args.names)
    print(map)

    col_names = list(species_abundance.columns)
    final_col = col_names.index("superkingdom")
    print(col_names)
    sample_list = col_names[final_col + 1::]
    for i in range(0, len(sample_list)):
        header = build_header(sample_list[i])
        body = build_body(col_names[0:final_col+1], species_abundance, sample_list[i], map)
        break

def build_body(colnames, data, percentage_col, names):
    tax_map = {}
    colnames.reverse()
    for colname_i in range(0, len(colnames)):
        print(colname_i)
        print(colnames[colname_i])
        uniques = data[colnames[colname_i]].unique().tolist()
        for unique_ in uniques:
            temp_body = ""
            print(unique_)
            relevant_data = data[data[colnames[colname_i]] == unique_]
            percentage = relevant_data[percentage_col].sum() * 100
            print(percentage)
            id = names["id"][names["name"] == unique_].tolist()[0]
            print(id)
            tax_map[unique_] = id

            # TODO loop terug over vorige classes, en vind die ID to make lineage




        break
    return 2



def build_header(sampleID):
    header = f"""# Taxonomic profiling output
@SampleID:{sampleID}
@Version:0.9.1
@Ranks:superkingdom|phylum|class|order|family|genus|species
@@TAXID	RANK	TAXPATH	TAXPATHSN	PERCENTAGE
"""
    return header