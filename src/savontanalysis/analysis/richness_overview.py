import re
import numpy as np
import pandas as pd

from savontanalysis.io import read_species_abundance, read_tab_pandas


def register(subparsers):
    """
    Registers a new subparser for richness overview arguments
    :param subparsers: Subparser from cli.py
    :return: -
    """
    p = subparsers.add_parser(
        "richness_overview",
        help="Get an overview of the assignments in Savont generated output")
    p.add_argument(
        "--input_dir",
        required=True,
        help="Savont classifiy output directory")
    p.add_argument("--thresholds", nargs="+", default=[0, 0.1, 1, 5],
                   type=float,
                   help="List of thresholds "
                        "(regarding the relative abundance) "
                        "to use as a filter (in %%)")
    p.add_argument("--max_abundance", default=1, type=float,
                   help=f"Select the maximum relative abundance, "
                        f"any abundance below this will "
                        f"be considered rare default:{1}")
    p.add_argument("--min_reads", default=10, type=int,
                   help=f"Select the minimum amount of reads "
                        f"to be considered a rare species "
                        f"default:{10}")

    p.add_argument("--output", default="./richness.tsv")


def run(args):
    """
    The main function that gets called when
    the user wants to get a richness overview
    :param args: CLI arguments.
    :return: Writes a file containing the richness overview
    """

    asv = read_tab_pandas.main(f"{args.input_dir}/asv_mappings.tsv", header=0)
    abundance = read_species_abundance.main(args.input_dir)
    if asv is None or abundance is None:
        return
    total_depth = get_total_depth(asv)
    relative_abundance_columns = calculate_reads(total_depth, abundance)
    abundance_no_unclassified = drop_unclassified(abundance)
    recalculate_rel_abundance(abundance_no_unclassified,
                              relative_abundance_columns)
    richness = thresholds_filter(args.thresholds, abundance_no_unclassified,
                                 relative_abundance_columns)
    n_rare_species_list = n_rare_species(args.max_abundance, args.min_reads,
                                         abundance, relative_abundance_columns)
    shannon_exps = calc_exp_shannon(abundance_no_unclassified,
                                    relative_abundance_columns)
    inverse_simpsons = calc_inverse_simpson(abundance_no_unclassified,
                                            relative_abundance_columns)
    richness.extend([n_rare_species_list, shannon_exps, inverse_simpsons])
    columns = ["metrics"] + list(relative_abundance_columns)

    df = pd.DataFrame(richness)
    df.columns = columns
    df.to_csv(args.output, sep="\t")


def get_total_depth(asv):
    """
    Gets the total depth of an ASV mapping
    :param asv: ASV mapping dataframe
    :return: Returns the total depth
    """
    asv_headers = asv["asv_header"].unique()
    total_depth = 0
    for header in asv_headers:
        depth = int(header.split("-")[-1])
        total_depth += depth
    return total_depth


def calculate_reads(total_depth, abundance):
    """
    Calculates the abundance in numbers, instead of relative abundance.\n
    Adds new columns to dataframe that hold this value
    :param total_depth: The total depth of a mapping
    :param abundance: Species abundance dataframe
    :return: The names of the columns containing the relative abundance
    """
    sk_index = abundance.columns.get_loc("superkingdom")
    cols_after_sk = abundance.columns[sk_index+1:]

    for col in cols_after_sk:
        abundance[f"{col}_reads"] = abundance[col] * total_depth

    return cols_after_sk


def drop_unclassified(abundance):
    """
    Drops all rows that contains UNKNOWN or UNCLASSIFIED
    :param abundance: Species abundance dataframe
    :return: Returns the abundance, with UNKNOWN and UNCLASSIFIED removed
    """
    strings = ["UNKNOWN", "UNCLASSIFIED"]
    pattern = "|".join(re.escape(s) for s in strings)
    str_columns = abundance.select_dtypes(include="object").columns
    mask = abundance[str_columns].apply(lambda col: col.str.contains(
        pattern, case=False, na=False)).any(axis=1)
    return abundance[~mask]


def recalculate_rel_abundance(abundance, relative_abundance_columns):
    """
    Recalculates the relative abundance of after removing rows from it
    Updates the relative abundance columns
    already found in the abundance dataframe.

    :param abundance: Species abundance dataframe
    :param relative_abundance_columns: List of columns that
    contain the relative abundance
    :return:
    """
    for col in relative_abundance_columns:
        total = abundance[f"{col}_reads"].sum()
        if total == 0:
            abundance[col] = 0
            continue

        abundance[col] = abundance[f"{col}_reads"] / total


def thresholds_filter(thresholds, abundance, relative_abundance_columns):
    """
    Filters the abundance dataframe relative abundance
    based on different thresholds
    :param thresholds: List of thresholds
    :param abundance: Species abundance dataframe
    :param relative_abundance_columns: list of columns
    containing relative abundance columns
    :return: List containing the number of species, for every threshold
    """
    lijstje = []
    for t in thresholds:
        temp_lijst = [f"rel >= {t}"]
        for column in relative_abundance_columns:
            number_of_species_above_t = (abundance[column]*100 >= t).sum()
            temp_lijst.append(int(number_of_species_above_t))
        lijstje.append(temp_lijst)
    return lijstje


def n_rare_species(max_rel_abundance, min_n_reads, abundance, columns):
    """
    FInds the amount of rare species in a dataframe based on
    the relative abundance and amount of reads
    :param max_rel_abundance: Maximum relative abundance
    a rare species can have
    :param min_n_reads: Minimum amount of reads a rare species should have
    :param abundance: Species abundance dataframe
    :param columns: List of columns that contain the relative abundance
    :return: A list of number of rare species
    """
    n_rare_species_list = [f"rare_species rel < {max_rel_abundance},"
                           f" reads >= {min_n_reads}"]
    for col in columns:
        n_species = ((abundance[col]*100 <= max_rel_abundance) &
                     (abundance[f"{col}_reads"] >= min_n_reads)).sum()
        n_rare_species_list.append(int(n_species))
    return n_rare_species_list


def calc_exp_shannon(abundance, relative_abundance_columns):
    """
    Calculates the exponential Shannon metric
    :param abundance: Species abundance dataframe
    :param relative_abundance_columns: List of columns that
    contain the relative abundance
    :return: A list containing the shannon exp for every sample
    """
    shannon_exps = ["exp_shannon"]
    for col in relative_abundance_columns:
        p = abundance[col]

        total = -(p * np.log(p.where(p > 0))).sum()
        if total == 0:
            shannon_exp = np.nan
        else:
            shannon_exp = np.exp(total)
        shannon_exps.append(float(shannon_exp))
    return shannon_exps


def calc_inverse_simpson(abundance, relative_abundance_columns):
    """
    Calculates inverse simpson metric
    :param abundance: Species abundance dataframe
    :param relative_abundance_columns: List of columns that
    contain the relative abundance
    :return: A list containing the inverse simpson for every sample
    """
    inverse_simpsons = ["inverse_simpson"]
    for col in relative_abundance_columns:
        p = abundance[col]

        total = (p**2).sum()
        if total == 0:
            inv_simpson = np.nan
        else:
            inv_simpson = 1 / total
        inverse_simpsons.append(float(inv_simpson))
    return inverse_simpsons
