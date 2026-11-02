from collections import defaultdict
import pandas as pd
def main(asv_mapping):
    print("_---------_----__--")
    asv_to_lineage = asv_mapping.groupby("asv_header", sort=False)[["lineage", "alignment_identity"]].agg(list)
    filtered = asv_to_lineage.apply(
        lambda row: filter_max_pair(row["lineage"], row["alignment_identity"]), axis = 1)
    asv_to_lineage['lineage'] = [f[0] for f in filtered]
    asv_to_lineage['alignment_identity'] = [f[1] for f in filtered]

    resolved_lineages = resolve_all_lineages(asv_to_lineage["lineage"])

    return resolved_lineages


def resolve_all_lineages(asv_to_lineage):
    asv_sets = {asv: set(lineages) for asv, lineages in asv_to_lineage.items()}

    resolved_lineages = {}
    for asv, lineages in asv_to_lineage.items():
        print()

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
    m = max(alignment_identity)
    kept = [(lin, identity) for lin, identity in zip(lineage, alignment_identity) if identity == m]

    return [l for l, _ in kept], [i for _, i in kept]


def create_lineage_to_asv(asv_to_lineage):
    lineage_to_asv = defaultdict(list)
    for asv, lineages in asv_to_lineage.items():
        for lineage in lineages:
            lineage_to_asv[lineage].append(asv)
    return lineage_to_asv

def find_all_single_candidates(asv_to_lineage):
    return asv_to_lineage[asv_to_lineage.apply(len) == 1]