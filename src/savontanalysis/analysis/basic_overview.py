from savontanalysis.io import read_species_abundance
from savontanalysis.viz import relative_abundance
from savontanalysis.viz import sunburst
from savontanalysis.io import write_plot
def register(subparsers):
    p = subparsers.add_parser("basic_overview", help="Basic overview of a classify run")
    p.add_argument("--input_dir", required=True)
    p.add_argument("--output_dir", default="./")
    p.add_argument("--top", help = "Filter data to only include top x species (default = all data)", default = 0, type = int)

def run(args):
    species_abundance = read_species_abundance.main(args.input_dir)
    if species_abundance is None:
        return
    fig_rel_ab = relative_abundance.create_abundance_plot(species_abundance, "species", args.top)
    write_plot.write(fig_rel_ab, args.output_dir, "abundance_plot.png")

    fig_sunburst = sunburst.create_sunburst_plot(species_abundance)
    write_plot.write(fig_sunburst, args.output_dir, "sunburst.html")

