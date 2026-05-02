import pytest

from boolean_ri.loaders.txt_loader import load_txt_directory, load_txt_file


def test_load_txt_file_reads_content(tmp_path) -> None:
    file = tmp_path / "document.txt"
    file.write_text("python boolean search", encoding="utf-8")

    assert load_txt_file(str(file)) == "python boolean search"


def test_load_txt_file_missing_file_raises_file_not_found_error(tmp_path) -> None:
    file = tmp_path / "missing.txt"

    with pytest.raises(FileNotFoundError):
        load_txt_file(str(file))


def test_load_txt_file_reads_empty_file(tmp_path) -> None:
    file = tmp_path / "empty.txt"
    file.write_text("", encoding="utf-8")

    assert load_txt_file(str(file)) == ""


def test_load_txt_file_reads_utf8_content(tmp_path) -> None:
    file = tmp_path / "accented.txt"
    file.write_text("configuración búsqueda información ação", encoding="utf-8")

    assert load_txt_file(str(file)) == "configuración búsqueda información ação"


def test_load_txt_file_rejects_non_txt_extension(tmp_path) -> None:
    file = tmp_path / "document.md"
    file.write_text("not supported", encoding="utf-8")

    with pytest.raises(ValueError):
        load_txt_file(str(file))


def test_load_txt_directory_loads_only_txt_files(tmp_path) -> None:
    txt_file = tmp_path / "document.txt"
    md_file = tmp_path / "notes.md"
    txt_file.write_text("indexed content", encoding="utf-8")
    md_file.write_text("ignored content", encoding="utf-8")

    assert load_txt_directory(str(tmp_path)) == {"document.txt": "indexed content"}


def test_load_txt_directory_missing_path_raises_file_not_found_error(tmp_path) -> None:
    missing_directory = tmp_path / "missing"

    with pytest.raises(FileNotFoundError):
        load_txt_directory(str(missing_directory))
