import json
from pathlib import Path


def load_plan(path):
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return []
    records = json.loads(text)
    if not isinstance(records, list):
        raise ValueError("Plan must contain a list")
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("Each session must be a dictionary")
        if (
            not isinstance(record.get("topic"), str)
            or not record["topic"].strip()
        ):
            raise ValueError("Each session needs a topic")
        if type(record.get("minutes")) is not int or record["minutes"] < 0:
            raise ValueError("Minutes must be nonnegative integers")
    return records


def save_new_plan(path, records):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(records, stream, indent=2, ensure_ascii=False)
        stream.write("\n")


if __name__ == "__main__":
    path = Path("practice-plan.json")
    if not path.exists():
        save_new_plan(path, [{"topic": "files", "minutes": 25}])
    sessions = load_plan(path)
    print(f"Stored sessions: {len(sessions)}")
    print(f"Total minutes: {sum(row['minutes'] for row in sessions)}")
