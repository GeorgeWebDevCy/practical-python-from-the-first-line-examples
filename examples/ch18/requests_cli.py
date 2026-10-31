import argparse
import json
from pathlib import Path
from tempfile import NamedTemporaryFile

from examples.ch17.board import load_requests


def save_requests(path, records):
    temporary = None
    try:
        with NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=path.parent,
            prefix=".requests-",
            suffix=".tmp",
            delete=False,
        ) as stream:
            temporary = Path(stream.name)
            json.dump(records, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
        temporary.replace(path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()


def add_request(path, title):
    title = title.strip()
    if not title:
        raise ValueError("Title is required")
    records = load_requests(path)
    identifier = max((row["id"] for row in records), default=0) + 1
    records.append({"id": identifier, "title": title, "done": False})
    save_requests(path, records)
    return identifier


def complete_request(path, identifier):
    records = load_requests(path)
    for row in records:
        if row["id"] == identifier:
            row["done"] = True
            save_requests(path, records)
            return
    raise ValueError("Request ID was not found")


def main():
    parser = argparse.ArgumentParser(
        description="Maintain a local request list"
    )
    parser.add_argument("--data", type=Path, default=Path("requests.json"))
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add")
    add.add_argument("title")
    commands.add_parser("list")
    done = commands.add_parser("done")
    done.add_argument("identifier", type=int)
    args = parser.parse_args()
    try:
        if args.command == "add":
            identifier = add_request(args.data, args.title)
            print(f"Added request #{identifier}")
        elif args.command == "done":
            complete_request(args.data, args.identifier)
            print(f"Completed request #{args.identifier}")
        else:
            records = load_requests(args.data)
            if not records:
                print("No requests yet.")
            for row in records:
                status = "done" if row["done"] else "open"
                print(f"#{row['id']} [{status}] {row['title']}")
    except (OSError, ValueError) as error:
        parser.exit(1, f"Cannot update requests: {error}\n")


if __name__ == "__main__":
    main()
