from email.policy import default
from random import choices

from savontanalysis.io import read_species_abundance
from savontanalysis.viz import relative_abundance
from savontanalysis.viz import sunburst
from savontanalysis.io import write_plot
def register(subparsers):
    p = subparsers.add_parser("basic_overview", help="Basic overview of a classify run")
    p.add_argument("--input_dir", required=True)
    p.add_argument("--output_dir", default="./")
    p.add_argument("--top", help = "Filter data to only include top x species (default = all data)", default = 0, type = int)
    p.add_argument("--taxonomic_rank", help = "Taxonomic rank to use as abundance value",
                   choices = ["species", "genus"], default = "species"),
    p.add_argument("--db", help = "What database was used with Savont",
                   choices = ["silva", "greengenes"], default = "silva")



def run(args):
    species_abundance = read_species_abundance.main(args.input_dir)
    if species_abundance is None:
        return
    col_names = list(species_abundance.columns)
    final_col = col_names.index("superkingdom")
    sample_list = col_names[final_col + 1::]
    if args.db == "silva":
        cols = species_abundance["species"].str.split(" ", n = 1, expand = True)
        species_abundance['genus'] = cols[0]
    fig_rel_ab = relative_abundance.create_abundance_plot(species_abundance, args.taxonomic_rank, args.top)
    write_plot.write(fig_rel_ab, args.output_dir, "abundance_plot.png")

    for sample in sample_list:
        fig_sunburst = sunburst.create_sunburst_plot(species_abundance, sample, args.db)
        write_plot.write(fig_sunburst, args.output_dir, f"{sample}_sunburst.html")

