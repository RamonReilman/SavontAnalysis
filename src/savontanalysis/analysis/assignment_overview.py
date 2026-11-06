import pandas as pd
from savontanalysis.io import read_tab_pandas, dir_check
from savontanalysis.result_merging import tie_breaking_system, savont_result_merging


def register(subparsers):
    """
    Registers a new subparser for assignment overview arguments
    :param subparsers: Subparser from cli.py
    :return: -
    """
    p = subparsers.add_parser(
        "assignment_overview",
        help="Get an overview of the assignments in Savont generated output")
    p.add_argument(
        "--input_dir",
        required=True,
        help="Savont classifiy output directory")
    p.add_argument("--output", default="./assignment.tsv")


def run(args):
    """
    Generates 3 kinds of percentages for all taxonomic ranks:
    - Assignment %, % of strings not containing UNCLASSIFIED, UNKNOWN, NaN
    - Informative %, % of strings not containing:
        UNCLASSIFIED, UNKNOWN, NaN,
        Any string with X at the end, Incertae Sedis
    - Environmental %, % of strings containing uncultured, metagenome

    :param args: Arguments from the command line
    :return: Writes file at the arg.output
        """

    asv = read_tab_pandas.main(f"{args.input_dir}/asv_mappings.tsv", header=0)
    if asv is None:
        return
    if dir_check.main(args.output) is False:
        return
    savont_result_merging.create_lineage(asv)
    asv = tie_breaking_system.main(asv_mapping=asv)
    asv = pd.Series(asv).str.split(";", expand = True)
    asv.columns = ['Species', 'Genus', 'Family', 'Order', 'Class', 'Phylum', 'clade', 'superkingdom']
    asv.index.name = 'ASV_id'
    asv = asv.reset_index()
    asv = asv.replace('nan', pd.NA).dropna(how = "all", axis = 1)
    taxo_ranks = asv.iloc[:, 1: ]
    assignment_percentage = taxo_ranks.apply(calculate_assignment_perc)
    informative_percentage = taxo_ranks.apply(calculate_informative_perc)
    env_percentage = taxo_ranks.apply(calculate_environmental_perc)
    results = pd.DataFrame({
        "rank": assignment_percentage.index,
        "assignment %": assignment_percentage.values,
        "informative %": informative_percentage.values,
        "environmental %": env_percentage.values
    })
    results.to_csv(args.output, sep="\t", header=True, index=False)


def calculate_assignment_perc(col):
    """
    Calculates the assignment percentage
    :param col: column of a dataframe
    :return: returns the assignment percentage of the column
    """
    UNASSIGNED = ["UNCLASSIFIED", "UNKNOWN"]
    UNASSIGNED_PATTERN = "|".join(UNASSIGNED)
    return calculate_perc(col, UNASSIGNED_PATTERN)


def calculate_environmental_perc(col):
    """
    Calculates the environmental percentage
    :param col: column of a dataframe
    :return: returns the environmental percentage of the column
    """
    ENVIRONMENTAL_PATTERN = "|".join([
        r"uncultured",
        r"\bmetagenome\b",
    ])
    return 100 - calculate_perc(col, ENVIRONMENTAL_PATTERN, na=False)


def calculate_informative_perc(col):
    """
    Calculates the informative percentage
    :param col: column of a dataframe
    :return: returns the informative percentage of the column
    """
    UNASSIGNED = [
        r"UNCLASSIFIED",
        r"UNKNOWN",
        r"\bX{1,2}\b",  # X or XX
        r"Incertae[ _]Sedis",
    ]
    UNASSIGNED_PATTERN = "|".join(UNASSIGNED)
    return calculate_perc(col, UNASSIGNED_PATTERN)


def calculate_perc(col, pattern, na=True):
    """
    Calculates the percentage of a dataframe column, based on a regex pattern
    :param col: column of a dataframe
    :param pattern: regex pattern to find all wanted rows
    :param na: boolean to enable or disable the counting of NaN values
    :return: The calculated percentage
    """
    n = len(col)
    assignment_perc = (n - col.str.contains(
        pattern, na=na, regex=True).sum()) / n * 100
    return assignment_perc
