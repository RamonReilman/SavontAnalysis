import argparse

from savontanalysis.analysis import basic_overview


def setup_cli():
    parser = argparse.ArgumentParser(description="Savont metagenomics analyser")
    subparsers = parser.add_subparsers(dest="type", required=True,
                                       help="Pick what kind of analysis you want")

    basic_overview.register(subparsers)
    return parser.parse_args()

def main(argv = None):
    args = setup_cli()
    dispatch = {"basic_overview": basic_overview.run}
    dispatch[args.type](args)