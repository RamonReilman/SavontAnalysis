import argparse
import platform
from savontanalysis.analysis import basic_overview
from savontanalysis.taxonomy import profile2CAMI
from savontanalysis.custom_db_gen import custom_db_gen
from savontanalysis.db_merging import db_merge


def setup_cli():
    parser = argparse.ArgumentParser(description="Savont metagenomics analyser")
    subparsers = parser.add_subparsers(dest="type", required=True,
                                       help="Pick what kind of analysis you want")

    basic_overview.register(subparsers)
    profile2CAMI.register(subparsers)
    custom_db_gen.register(subparsers)
    db_merge.register(subparsers)

    return parser.parse_args()

def main(argv = None):
    args = setup_cli()
    if platform.system() == "Windows":
        print("Tool not compatible with Windows")
        return
    dispatch = {"basic_overview": basic_overview.run,
                "profile2CAMI": profile2CAMI.run,
                "customdb": custom_db_gen.run,
                "mergeDB": db_merge.run}
    dispatch[args.type](args)