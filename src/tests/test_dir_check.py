import pytest
from pathlib import Path
from savontanalysis.io import dir_check

def test_existing_dir(tmp_path):
    dir_check.main(str(tmp_path))
    assert tmp_path.is_dir()


def test_missing_path_created(tmp_path):
    target = tmp_path / "a" / "b" / "c"
    assert not target.exists()
    dir_check.main(str(target))
    assert target.is_dir()


def test_file_path_creates_parent_not_file(tmp_path):
    target = tmp_path / "subdir" / "note.txt"
    assert not target.parent.exists()
    dir_check.main(str(target))
    assert not target.exists()
    assert target.parent.is_dir()


def test_permission_error_returns_false(monkeypatch, tmp_path):
    def always_fail(*args, **kwargs):
        raise PermissionError("denied")

    monkeypatch.setattr(Path, "mkdir", always_fail)
    with pytest.raises(PermissionError, match="denied"):
        dir_check.main(str(tmp_path / "newdir"))
