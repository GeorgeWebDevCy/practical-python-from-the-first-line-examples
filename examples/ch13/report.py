import csv
from io import StringIO

SAMPLE = """category,cents
materials,1250
travel,300
materials,250
travel,unknown
"""


def summarise(stream):
    reader = csv.DictReader(stream)
    if reader.fieldnames != ["category", "cents"]:
        raise ValueError("Expected category,cents header")
    totals = {}
    rejected = []
    for row_number, row in enumerate(reader, start=2):
        category = (row.get("category") or "").strip()
        try:
            amount = int(row.get("cents") or "")
            if not category or amount < 0 or None in row:
                raise ValueError("Invalid row")
        except ValueError:
            rejected.append(row_number)
            continue
        totals[category] = totals.get(category, 0) + amount
    return totals, rejected


if __name__ == "__main__":
    totals, rejected = summarise(StringIO(SAMPLE))
    for category, cents in sorted(totals.items()):
        print(f"{category}: {cents // 100}.{cents % 100:02d}")
    print(f"Rejected rows: {rejected}")
