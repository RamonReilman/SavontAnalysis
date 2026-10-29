from collections import defaultdict
from typing import Any

from numpy import dtype, ndarray
from pandas import DataFrame, Series
from pandas.core.arrays import ExtensionArray
from pandas.io.parsers import TextFileReader
from savontanalysis.result_merging.tie_breaking_system import resolve_all_lineages

from savontanalysis.io import read_tab_pandas

def main(clean_lineages, final_assignments, feature_table):

    extract_barcodes(final_assignments)
    barcodes = final_assignments["barcode"].unique()
    barcodes_n_counts = get_barcode_counts(feature_table)

    lineage_abundance = calculate_abundancies(clean_lineages, barcodes_n_counts, final_assignments)

    return lineage_abundance


def calculate_abundancies(resolved_lineages, barcodes_n_counts,
                          final_assignments):

    lineage_to_asv = defaultdict(list)
    for asv, lineage in resolved_lineages.items():
        lineage_to_asv[lineage].append(asv)
    lineage_abundance = {}
    for barcode in barcodes_n_counts.keys():
        lineage_abundance[barcode] = {}
        for lineage, asvs in lineage_to_asv.items():
            print(lineage)
            print(asvs)
            count = get_count(asvs)

            if barcodes_n_counts[barcode] > 0:
                lineage_abundance[barcode][lineage] = count / (barcodes_n_counts[barcode])
                continue
            lineage_abundance[barcode][lineage] = 0
    return lineage_abundance


def get_barcode_counts(feature_table):

    dict_barcodes = feature_table.drop(columns=["#OTU ID"]).sum().to_dict()
    return {k.replace("_", ""): v for k, v in dict_barcodes.items()}



def get_count(asvs):
    total = 0
    for depth in asvs:
        depth_int = int(depth.split("-")[-1])
        total += depth_int
    return total


def extract_barcodes(df):
    df["barcode"] = df.iloc[:, 0].str.extract(r"\bbarcode=(\S+)")
