"""File I/O for the life assistant data store."""
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
PROMPTS_DIR = BASE_DIR / "prompts"


def read(path: str) -> str:
    return (BASE_DIR / path).read_text(encoding="utf-8")


def write(path: str, content: str) -> None:
    target = BASE_DIR / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def append_entry(module: str, entry: str) -> None:
    path = DATA_DIR / module / "index.md"
    with path.open("a", encoding="utf-8") as f:
        f.write(f"\n{entry}\n")


def read_lines(path: str) -> list[str]:
    return (BASE_DIR / path).read_text(encoding="utf-8").splitlines()


def exists(path: str) -> bool:
    return (BASE_DIR / path).exists()
