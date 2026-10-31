"""Reference exercise behaviours. Read after attempting the chapter exercises.

Functions collect solutions in one testable place; early exercises can be
written as straight-line scripts before functions are introduced in Chapter 7.
"""
import csv
from datetime import date
from html import escape

from examples.ch12.organise import classify
from examples.ch15.lending import LoanItem
from examples.ch16.fetch import fetch_sessions
from examples.ch17.board import render_page
from examples.toolkit.durations import session_total


def trip_estimate(distance_km=30, speed_kmh=15, stop_minutes=20):
    travel = distance_km / speed_kmh * 60
    return travel, travel + stop_minutes


def lesson_plan(name, minutes_text):
    return name.strip(), int(minutes_text.strip()) + 3


def workshop_message(hour):
    if hour < 0 or hour > 23:
        return "Invalid hour"
    if 9 <= hour < 16:
        return "Drop-offs accepted"
    return "Workshop closed"


def reading_plan():
    topics = ["files", "loops", "tests"]
    session = {"topic": topics[1], "minutes": 20}
    tags = {"practice", "beginner", "practice"}
    return topics[1], session["minutes"], len(tags), session.get("notes", "No notes")


def checklist(items):
    if not items:
        return "Nothing to pack."
    return "\n".join(f"{number}. {item}" for number, item in enumerate(items, start=1))


def classify_with_data(path):
    if path.suffix.lower() in {".csv", ".json"}:
        return "data"
    return classify(path)


def two_sessions(first, second):
    return session_total(first), session_total(second)


def summarise_counts(stream):
    reader = csv.DictReader(stream)
    if reader.fieldnames != ["category", "cents"]:
        raise ValueError("Expected category,cents header")
    summary, rejected = {}, []
    for number, row in enumerate(reader, start=2):
        category = (row.get("category") or "").strip()
        try:
            amount = int(row.get("cents") or "")
            if not category or amount < 0 or None in row:
                raise ValueError("Invalid row")
        except ValueError:
            rejected.append(number)
            continue
        entry = summary.setdefault(category, {"cents": 0, "count": 0})
        entry["cents"] += amount
        entry["count"] += 1
    return summary, rejected


class CountedLoanItem(LoanItem):
    def __init__(self, title):
        super().__init__(title)
        self.checkout_count = 0

    def checkout(self, borrower):
        super().checkout(borrower)
        self.checkout_count += 1


def fetch_with_daily_limit(url, limit):
    records = fetch_sessions(url)
    if sum(row["minutes"] for row in records) > limit:
        raise ValueError("Daily limit exceeded")
    return records


def render_with_count(records):
    count = sum(not row["done"] for row in records)
    return render_page(records).replace("<ul>", f"<p>Open requests: {count}</p><ul>", 1)


def parse_due_date(text):
    parsed = date.fromisoformat(text)
    if parsed.isoformat() != text:
        raise ValueError("Use YYYY-MM-DD")
    return parsed
