from collections import defaultdict
import pandas as pd
def main(asv_mapping):
    print("_---------_----__--")
    asv_to_lineage = asv_mapping.groupby("asv_header", sort=False)["lineage"].agg(list)

    resolved_lineages = resolve_all_lineages(asv_to_lineage)

    return resolved_lineages


def resolve_all_lineages(asv_to_lineage):
    asv_sets = {asv: set(lineages) for asv, lineages in asv_to_lineage.items()}

    resolved_lineages = {}
    for asv, lineages in asv_to_lineage.items():

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




def create_lineage_to_asv(asv_to_lineage):
    lineage_to_asv = defaultdict(list)
    for asv, lineages in asv_to_lineage.items():
        for lineage in lineages:
            lineage_to_asv[lineage].append(asv)
    return lineage_to_asv

def find_all_single_candidates(asv_to_lineage):
    return asv_to_lineage[asv_to_lineage.apply(len) == 1]