from pathlib import Path


def load_txt_file(path: str) -> str:
    file = Path(path)

    if file.suffix != ".txt":
        raise ValueError("Only .txt files are supported")

    return file.read_text(encoding="utf-8")


def load_txt_directory(path: str) -> dict[str, str]:
    docs = {}
    base = Path(path)

    if not base.exists():
        raise FileNotFoundError(path)

    for file in base.glob("*.txt"):
        docs[file.name] = load_txt_file(str(file))

    return docs
