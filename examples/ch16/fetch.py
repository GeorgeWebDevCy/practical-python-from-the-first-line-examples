import argparse
import json
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


def fetch_sessions(url):
    parsed = urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("Use an HTTP or HTTPS URL")
    request = Request(url, headers={"Accept": "application/json"})
    with urlopen(request, timeout=3) as response:
        if response.headers.get_content_type() != "application/json":
            raise ValueError("Expected application/json")
        body = response.read(65537)
    if len(body) > 65536:
        raise ValueError("Response is too large for this client")
    records = json.loads(body.decode("utf-8"))
    if not isinstance(records, list):
        raise ValueError("Expected a list of sessions")
    for record in records:
        if not isinstance(record, dict):
            raise ValueError("Invalid session record")
        if not isinstance(record.get("topic"), str) or not record["topic"].strip():
            raise ValueError("Session topic is required")
        if type(record.get("minutes")) is not int or record["minutes"] < 0:
            raise ValueError("Session minutes must be nonnegative integers")
    return records


def main():
    parser = argparse.ArgumentParser(description="Read sessions from an HTTP service")
    parser.add_argument("url")
    args = parser.parse_args()
    try:
        sessions = fetch_sessions(args.url)
    except (OSError, ValueError) as error:
        parser.exit(1, f"Cannot fetch sessions: {error}\n")
    print(f"Sessions received: {len(sessions)}")
    print(f"Total minutes: {sum(row['minutes'] for row in sessions)}")


if __name__ == "__main__":
    main()
