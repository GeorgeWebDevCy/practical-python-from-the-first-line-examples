import argparse
from html import escape
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path


def load_requests(path):
    try:
        records = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return []
    if not isinstance(records, list):
        raise ValueError("Requests must be a list")
    seen = set()
    for row in records:
        if not isinstance(row, dict):
            raise ValueError("Invalid request")
        identifier = row.get("id")
        if type(identifier) is not int or identifier <= 0 or identifier in seen:
            raise ValueError("IDs must be unique positive integers")
        if not isinstance(row.get("title"), str) or not row["title"].strip():
            raise ValueError("Title is required")
        if type(row.get("done")) is not bool:
            raise ValueError("Completion flag must be Boolean")
        seen.add(identifier)
    return records


def render_page(records):
    items = []
    for row in records:
        status = "done" if row["done"] else "open"
        items.append(f'<li>#{row["id"]} {escape(row["title"])} — {status}</li>')
    content = "".join(items) if items else "<li>No requests yet.</li>"
    return ('<!doctype html><html lang="en"><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Local request board</title><body><h1>Local request board</h1>'
            '<p>Read-only view. Refresh after command-line updates.</p>'
            f'<ul>{content}</ul></body></html>')


class BoardHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_error(404, "Not found")
            return
        try:
            records = load_requests(self.server.data_path)
            body = render_page(records).encode("utf-8")
        except (OSError, ValueError):
            self.send_error(500, "Cannot read board data")
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        pass


def main():
    parser = argparse.ArgumentParser(description="View a local read-only request board")
    parser.add_argument("--data", type=Path, default=Path("requests.json"))
    parser.add_argument("--port", type=int, default=8766)
    args = parser.parse_args()
    with ThreadingHTTPServer(("127.0.0.1", args.port), BoardHandler) as server:
        server.data_path = args.data.resolve()
        print(f"Local board: http://127.0.0.1:{server.server_port}/", flush=True)
        try:
            server.serve_forever()
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    main()
