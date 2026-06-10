import tempfile
from pathlib import Path

from proxycraft.shared.utilities.path_compat import is_regular_file


def test_is_regular_file_for_existing_file():
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = Path(temp_dir) / "sample.txt"
        file_path.write_text("hello", encoding="utf-8")

        assert is_regular_file(file_path) is True


def test_is_regular_file_for_directory():
    with tempfile.TemporaryDirectory() as temp_dir:
        assert is_regular_file(Path(temp_dir)) is False


def test_is_regular_file_for_symlink():
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        real_file = root / "real.txt"
        real_file.write_text("hello", encoding="utf-8")
        symlink = root / "link.txt"
        try:
            symlink.symlink_to(real_file)
        except OSError:
            return

        assert is_regular_file(symlink) is False


def test_is_regular_file_for_missing_path():
    assert is_regular_file(Path("/tmp/does-not-exist-proxycraft-test")) is False
