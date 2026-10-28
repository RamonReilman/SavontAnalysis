from typing import Any

from numpy import dtype, ndarray
from pandas import DataFrame, Series
from pandas.core.arrays import ExtensionArray
from pandas.io.parsers import TextFileReader

from savontanalysis.io import read_tab_pandas

def main(asv_mapping, final_assignments):
    asv_mapping = asv_mapping.copy()
    final_assignments = final_assignments.copy()
    create_lineage(asv_mapping)
    asv_to_lineage = asv_mapping.groupby("lineage")["asv_header"].unique()

    extract_barcodes(final_assignments)
    barcodes = final_assignments["barcode"].unique()
    lineages = list(asv_to_lineage.index)[1:]
    barcodes_n_counts = get_barcode_counts(barcodes, final_assignments)
    print(barcodes_n_counts)

    lineage_abundance = calculate_abundancies(asv_to_lineage, barcodes_n_counts, final_assignments, lineages)

    return lineage_abundance


def calculate_abundancies(asv_to_lineage: Series, barcodes_n_counts: dict[Any, Any],
                          final_assignments: DataFrame | TextFileReader, lineages: list[Any]) -> dict[Any, Any]:
    lineage_abundance = {}
    for i, lineage in enumerate(lineages):
        asvs = asv_to_lineage.iloc[i]
        for barcode in barcodes_n_counts.keys():
            if barcode not in lineage_abundance:
                lineage_abundance[barcode] = {}
            asvs_filtered_count = len(final_assignments[(final_assignments.asv.isin(asvs)) &
                                                        (final_assignments["barcode"] == barcode)])
            print(asvs_filtered_count)
            if barcodes_n_counts[barcode] > 0:
                lineage_abundance[barcode][lineage] = asvs_filtered_count / barcodes_n_counts[barcode]
                continue
            lineage_abundance[barcode][lineage] = 0
    return lineage_abundance


def get_barcode_counts(barcodes, final_assignments):
    barcodes_n_counts = {}
    for barcode in barcodes:
        pass
        n_total = len(final_assignments[(final_assignments["asv"] != "unassigned") &
                                        (final_assignments["barcode"] == barcode)])
        barcodes_n_counts[barcode] = n_total
    return barcodes_n_counts


def create_lineage(df):
    cols = ["species", "genus", "family", "order", "class", "phylum",
       "clade", "superkingdom"]
    df["lineage"] = df[cols].apply(lambda row: ";".join(row.values.astype(str)), axis = 1)

def extract_barcodes(df):
    df["barcode"] = df.iloc[:, 0].str.extract(r"\bbarcode=(\S+)")
