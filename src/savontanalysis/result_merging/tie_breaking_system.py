from collections import defaultdict
import pandas as pd


def main(asv_mapping):
    """
    One main to rule the tie breaking system
    :param asv_mapping: ASV mapping dataframe
    :return: Returns a dict that contains all resolved lineages for the ASVs
    """
    asv_to_lineage = asv_mapping.groupby("asv_header", sort=False)[["lineage", "alignment_identity"]].agg(list)
    filtered = asv_to_lineage.apply(
        lambda row: filter_max_pair(row["lineage"],
                                    row["alignment_identity"]), axis=1)
    asv_to_lineage['lineage'] = [f[0] for f in filtered]
    asv_to_lineage['alignment_identity'] = [f[1] for
                                            f in filtered]

    resolved_lineages = resolve_all_lineages(asv_to_lineage["lineage"])

    return resolved_lineages


def resolve_all_lineages(asv_to_lineage):
    """
    The actual tie breaking system
    Figures out which lineage has to be
    chosen for an ASV with multiple candidates.

    :param asv_to_lineage: A grouping of all lineages, and align-identity
    for all ASV headers
    :return: Returns a dict containing the winning lineages for every ASV
    """
    asv_sets = {asv: set(lineages) for asv, lineages in asv_to_lineage.items()}

    resolved_lineages = {}
    for asv, lineages in asv_to_lineage.items():

        # If ASV has 1 candidate, pick that one
        if len(lineages) == 1:
            resolved_lineages[asv] = lineages[0]
            continue

        new_set = asv_sets[asv]
        winner = None
        for other_asv, other_lineage in asv_to_lineage.items():
            if other_asv == asv:
                continue
            if len(other_lineage) == 1 and asv_sets[other_asv] < new_set:
                winner = other_lineage[0]
                break
        resolved_lineages[asv] = winner if winner else lineages[-1]
    return resolved_lineages


def filter_max_pair(lineage, alignment_identity):
    """
    Filters out all candidates that do not have the highest alignment identity.
    :param lineage: List of lineages
    :param alignment_identity: List of alignment identities
    :return: 2 separate lists containing the filtered
    lineages and alignment identities.
    """
    m = max(alignment_identity)
    kept = [(lin, identity) for lin, identity in
            zip(lineage, alignment_identity) if identity == m]

    return [l for l, _ in kept], [i for _, i in kept]


def create_lineage_to_asv(asv_to_lineage):
    """
    Creates a dict containing lineages as keys
    and a list of ASVs as values
    :param asv_to_lineage: ASV mapping grouped by the ASV headers
    :return: A dict containing lineages as keys
    and a list of ASVs as values
    """
    lineage_to_asv = defaultdict(list)
    for asv, lineages in asv_to_lineage.items():
        for lineage in lineages:
            lineage_to_asv[lineage].append(asv)
    return lineage_to_asv


def find_all_single_candidates(asv_to_lineage):
    """
    Finds all ASVs with 1 candidate
    :param asv_to_lineage: ASV mapping grouped by the ASV headers
    :return: All asvs with one candidate
    """
    return asv_to_lineage[asv_to_lineage.apply(len) == 1]
