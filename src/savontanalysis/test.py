from savontanalysis.taxonomy.database import TaxonomyDB

db = TaxonomyDB('~/.local/share/tax.db')  # explicit path this time
expected_order = ["species", "genus", "family", "order", "class", "phylum", "superkingdom"]

rows = db.get_all()
species_rows = [r for r in rows if r[3] == "species"]

bad = []
for taxid, parent_id, name, rank in species_rows:
    chain_ranks = [rank]
    pid = parent_id
    while pid is not None:
        parent = db.fetch_with_id(pid)
        if parent is None:
            bad.append((name, "orphaned parent"))
            break
        chain_ranks.append(parent[3])
        pid = parent[1]
    if chain_ranks != expected_order[:len(chain_ranks)]:
        bad.append((name, chain_ranks))

print(f"{len(species_rows)} species checked, {len(bad)} broken chains")
for b in bad[:20]:
    print(b)