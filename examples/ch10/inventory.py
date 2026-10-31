from pathlib import Path
from tempfile import TemporaryDirectory


def plan_groups(folder):
    plans = []
    for path in sorted(folder.iterdir()):
        if path.is_symlink() or not path.is_file():
            continue
        suffix = path.suffix.lower()
        if suffix in {".txt", ".md"}:
            group = "notes"
        elif suffix in {".jpg", ".png"}:
            group = "images"
        else:
            group = "other"
        plans.append((path.name, group))
    return plans


if __name__ == "__main__":
    with TemporaryDirectory() as directory:
        folder = Path(directory)
        for name in ["readme.TXT", "photo.png", "archive.zip"]:
            (folder / name).write_text("practice data", encoding="utf-8")
        for name, group in plan_groups(folder):
            print(f"{name} -> {group}/{name}")
