## Use:
```bash
pip install -e .
```

```bash
savont-analyse basic_overview --input_dir /home/redman/jaar4/savont_taxo_greengenes2
```

### Submodules:
#### basic_overview
Gives a basic overview of Savont results, like a barchart, and sunburst plot.

*Command line arguments*:
- --input_dir, Savont classify directory
- --output_dir, Directory where plots should be written to
- --top, Filter data to use the top X amount of species
- --taxonomic_rank, The taxonomic rank to use for abundance chart (`species` or `genus`)
- --db, the db used (either `silva` or `greengenes`)

#### profile2CAMI
Rewrites any WF-16s or Savont abundance output into a CAMI2 file format. This format is supported by OPAL (A tool to evaluate and compare different results).

*Command line arguments*:
- --input_dir, Savont classify directory
- --output_dir, Directory where plots should be written to
- --tool, the tool used to generate the input (`savont`, `wf-16s`, `nanosim`)
- --sampleID, name of sampleID in the header, should be the same for all files during an opal run.