from collections import defaultdict


def main(clean_lineages, final_assignments, feature_table):
    """
    Calculates the abundancies for all lineages
    :param clean_lineages: dict with asv as key,
        with the value being the chosen lineage
    :param final_assignments: DF of the Final assignments file
    :param feature_table: DF of the feature table file
    :return: dict of the abundance of every lineage, for every sample
    """
    extract_barcodes(final_assignments)
    barcodes_n_counts = get_barcode_counts(feature_table)

    lineage_abundance = calculate_abundancies(clean_lineages,
                                              barcodes_n_counts)

    return lineage_abundance


def calculate_abundancies(resolved_lineages, barcodes_n_counts):
    """
    Calculates the abundancies for all lineages
    :param resolved_lineages: dict with asv as key,
        with the value being the chosen lineage
    :param barcodes_n_counts: dict of total counts for each sample (barcode)
    :return: dict of the abundance of every lineage, for every sample
    """

    lineage_to_asv = defaultdict(list)
    for asv, lineage in resolved_lineages.items():
        lineage_to_asv[lineage].append(asv)
    lineage_abundance = {}
    for barcode in barcodes_n_counts.keys():
        lineage_abundance[barcode] = {}
        for lineage, asvs in lineage_to_asv.items():
            count = get_count(asvs)

            if barcodes_n_counts[barcode] > 0:
                lineage_abundance[barcode][lineage] = (
                        count / (barcodes_n_counts[barcode]))
                continue
            lineage_abundance[barcode][lineage] = 0
    return lineage_abundance


def get_barcode_counts(feature_table):
    """
    Gets the total counts for all samples
    :param feature_table: DF of the feature table file
    :return: dict with sample name as key, and the total counts as value
    """
    dict_barcodes = feature_table.drop(columns=["#OTU ID"]).sum().to_dict()
    return {k.replace("_", ""): v for k, v in dict_barcodes.items()}


def get_count(asvs):
    """
    Gets the total depth count for an asv
    :param asvs: str with ASV name (includes the depth)
    :return: int of the total depth for this asv
    """
    total = 0
    for depth in asvs:
        depth_int = int(depth.split("-")[-1])
        total += depth_int
    return total


def extract_barcodes(feature_table):
    """
    creates barcodes name in feature thatble with correct naming convention.
    :param feature_table: DF of the feature table file
    """
    feature_table["barcode"] = (feature_table.iloc[:, 0]
                                .str.extract(r"\bbarcode=(\S+)"))
