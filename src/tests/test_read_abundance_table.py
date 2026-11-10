import pytest
from pathlib import Path
import pandas as pd
from savontanalysis.io import read_abundance_table

def test_reads_matching_file(tmp_path):
    (tmp_path / "s1_abundance_table_run1.tsv").write_text(
        "taxon\tcount\nA\t5\nB\t3\n"
    )

    df = read_abundance_table.main(tmp_path)
    assert list(df.columns) == ["taxon", "count"]
    assert len(df) == 2
    assert df.iloc[0]["taxon"] == "A"
    assert df.iloc[0]["count"] == 5


def test_no_matching_file_raises_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError, match="abundance_table"):
        read_abundance_table.main(str(tmp_path))


def test_nonexistent_dir_raises_file_not_found(tmp_path):
    target = tmp_path / "nope"
    with pytest.raises(FileNotFoundError, match="abundance_table"):
        read_abundance_table.main(str(target))


def test_empty_file_raises_empty_data_error(tmp_path):
    (tmp_path / "x_abundance_table_run2.tsv").write_text("")
    with pytest.raises(pd.errors.EmptyDataError):
        read_abundance_table.main(str(tmp_path))
