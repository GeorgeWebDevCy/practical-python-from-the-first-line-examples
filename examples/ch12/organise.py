import argparse
from pathlib import Path
import shutil


def classify(path):
    suffix = path.suffix.lower()
    if suffix in {".txt", ".md"}:
        return "notes"
    if suffix in {".png", ".jpg"}:
        return "images"
    return "other"


def organise(source, destination, apply=False):
    source = source.resolve()
    destination = destination.resolve()
    if not source.is_dir():
        raise ValueError("Source must be a directory")
    if destination == source or source in destination.parents:
        raise ValueError("Destination must be outside the source")
    if destination.exists():
        raise FileExistsError("Destination already exists")
    if not destination.parent.is_dir():
        raise ValueError("Destination parent must already exist")
    plans = []
    for path in sorted(source.iterdir()):
        if path.is_symlink() or not path.is_file():
            continue
        plans.append((path, Path(classify(path)) / path.name))
    if apply:
        destination.mkdir()
        for original, relative in plans:
            if original.is_symlink() or not original.is_file():
                raise OSError("Source changed after planning")
            target = destination / relative
            target.parent.mkdir(exist_ok=True)
            with original.open("rb") as incoming, target.open("xb") as outgoing:
                shutil.copyfileobj(incoming, outgoing)
    return [(path.name, relative.as_posix()) for path, relative in plans]


def main():
    parser = argparse.ArgumentParser(description="Preview or copy grouped files")
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    try:
        plans = organise(args.source, args.destination, args.apply)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Cannot organise: {error}\n")
    print("Copied files:" if args.apply else "Preview only:")
    if not plans:
        print("No ordinary files found.")
    for name, relative in plans:
        print(f"{name} -> {relative}")


if __name__ == "__main__":
    main()
