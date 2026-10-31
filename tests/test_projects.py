from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import StringIO
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from threading import Thread
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import urlopen
import xml.etree.ElementTree as ET

from examples.ch09.plan_store import load_plan, save_new_plan
from examples.ch10.inventory import plan_groups
from examples.ch12.organise import organise
from examples.ch13.report import summarise
from examples.ch14.chart import bar_chart
from examples.ch15.lending import LoanItem
from examples.ch16.fetch import fetch_sessions
from examples.ch17.board import BoardHandler, load_requests, render_page
from examples.ch18.requests_cli import add_request, complete_request, save_requests
from examples.toolkit.durations import session_total

ROOT = Path(__file__).resolve().parents[1]


@contextmanager
def serving(handler, **attributes):
    with ThreadingHTTPServer(("127.0.0.1", 0), handler) as server:
        for name, value in attributes.items():
            setattr(server, name, value)
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            yield f"http://127.0.0.1:{server.server_port}"
        finally:
            server.shutdown()
            thread.join(timeout=5)


def handler_for(body, content_type="application/json", status=200):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format, *args):
            pass
    return Handler


class StorageTests(unittest.TestCase):
    def test_round_trip_and_exclusive_creation(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "plan.json"
            self.assertEqual(load_plan(path), [])
            records = [{"topic": "café notes", "minutes": 25}]
            save_new_plan(path, records)
            self.assertEqual(load_plan(path), records)
            original = path.read_bytes()
            with self.assertRaises(FileExistsError):
                save_new_plan(path, [])
            self.assertEqual(path.read_bytes(), original)

    def test_bad_plans(self):
        for text in ("{bad", "{}", '["record"]', '[{"topic":"x","minutes":true}]',
                     '[{"topic":"","minutes":1}]', '[{"topic":"x","minutes":-1}]'):
            with self.subTest(text=text), TemporaryDirectory() as folder:
                path = Path(folder) / "bad.json"
                path.write_text(text, encoding="utf-8")
                with self.assertRaises(ValueError):
                    load_plan(path)

    def test_total_contract(self):
        self.assertEqual(session_total(25), 30)
        self.assertEqual(session_total(0, 0), 0)
        for pair in ((-1, 5), (1, -1), (True, 0), (1.5, 0)):
            with self.subTest(pair=pair), self.assertRaises(ValueError):
                session_total(*pair)


class OrganiserTests(unittest.TestCase):
    def test_preview_apply_and_preservation(self):
        with TemporaryDirectory() as folder:
            source = Path(folder) / "inbox"
            source.mkdir()
            (source / "note.TXT").write_bytes(b"sample\x00bytes")
            (source / "nested").mkdir()
            destination = Path(folder) / "result"
            self.assertEqual(plan_groups(source), [("note.TXT", "notes")])
            self.assertEqual(organise(source, destination), [("note.TXT", "notes/note.TXT")])
            self.assertFalse(destination.exists())
            organise(source, destination, apply=True)
            self.assertEqual((source / "note.TXT").read_bytes(), b"sample\x00bytes")
            self.assertEqual((destination / "notes/note.TXT").read_bytes(), b"sample\x00bytes")
            with self.assertRaises(FileExistsError):
                organise(source, destination, apply=True)
            self.assertFalse((destination / "nested").exists())

    def test_invalid_locations_and_empty(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            source = root / "source"
            source.mkdir()
            self.assertEqual(organise(source, root / "out"), [])
            for src, dest in ((root / "missing", root / "out"), (source, source),
                              (source, source / "nested"), (source, root / "missing/out")):
                with self.subTest(src=src, dest=dest), self.assertRaises(ValueError):
                    organise(src, dest)

    def test_command_failure(self):
        with TemporaryDirectory() as folder:
            result = subprocess.run([sys.executable, str(ROOT / "examples/ch12/organise.py"),
                                     "missing", "result"], cwd=folder, capture_output=True,
                                    text=True, timeout=10)
            self.assertEqual(result.returncode, 1)
            self.assertIn("Source must be a directory", result.stderr)


class ReportTests(unittest.TestCase):
    def test_grouping_quoting_rejections(self):
        text = 'category,cents\n"tools, shared",100\n"tools, shared",50\nx,0\nx,-1\nx,no\nx,1,extra\n,5\nx\n'
        self.assertEqual(summarise(StringIO(text)), ({"tools, shared": 150, "x": 0}, [5, 6, 7, 8, 9]))

    def test_headers(self):
        self.assertEqual(summarise(StringIO("category,cents\n")), ({}, []))
        for header in ("", "cents,category\n", "category,amount\n"):
            with self.subTest(header=header), self.assertRaises(ValueError):
                summarise(StringIO(header))

    def test_chart_ratios_and_edge_cases(self):
        text = bar_chart({"A & B": 1500, "Travel": 300})
        bars = [n for n in ET.fromstring(text).iter() if n.tag.endswith("rect") and n.get("x") == "230"]
        self.assertEqual([float(n.get("width")) for n in bars], [400, 80])
        self.assertIn("A &amp; B", text)
        self.assertIn("No accepted records.", bar_chart({}))
        self.assertIn('width="0.00"', bar_chart({"zero": 0}))
        for value in (-1, True, float("nan"), float("inf")):
            with self.subTest(value=value), self.assertRaises(ValueError):
                bar_chart({"bad": value})


class LendingTests(unittest.TestCase):
    def test_lifecycle_isolation_and_rejected_changes(self):
        item, other = LoanItem(" Field guide "), LoanItem("Other")
        item.checkout(" Sam ")
        self.assertEqual(item.status(), "Field guide: borrowed by Sam")
        self.assertIsNone(other.borrower)
        with self.assertRaises(ValueError):
            item.checkout("Alex")
        self.assertEqual(item.borrower, "Sam")
        item.return_item()
        self.assertEqual(item.status(), "Field guide: available")
        with self.assertRaises(ValueError):
            item.return_item()
        with self.assertRaises(ValueError):
            item.checkout(" ")
        self.assertIsNone(item.borrower)
        with self.assertRaises(ValueError):
            LoanItem("")


class HttpTests(unittest.TestCase):
    def test_success_and_rejected_responses(self):
        records = [{"topic": "files", "minutes": 25}]
        with serving(handler_for(json.dumps(records).encode())) as url:
            self.assertEqual(fetch_sessions(url), records)
        cases = [(b"bad", "application/json"), (b"[]", "text/html"), (b"{}", "application/json"),
                 (b"x" * 65537, "application/json"),
                 (b'[{"topic":"x","minutes":true}]', "application/json"), (b'["bad"]', "application/json")]
        for body, mime in cases:
            with self.subTest(body=body[:25]), serving(handler_for(body, mime)) as url:
                with self.assertRaises(ValueError):
                    fetch_sessions(url)
        with serving(handler_for(b"missing", status=404)) as url:
            with self.assertRaises(HTTPError) as error:
                fetch_sessions(url)
            error.exception.close()
        with self.assertRaises(ValueError):
            fetch_sessions("file:///private.json")

    def test_board_http_routes_escaping_and_bad_storage(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "requests.json"
            self.assertIn("No requests yet.", render_page([]))
            add_request(path, "Check <draft> & notes")
            with serving(BoardHandler, data_path=path) as url:
                with urlopen(url + "/", timeout=3) as response:
                    self.assertEqual(response.status, 200)
                    self.assertEqual(response.headers.get_content_type(), "text/html")
                    self.assertIn("Check &lt;draft&gt; &amp; notes", response.read().decode("utf-8"))
                with self.assertRaises(HTTPError) as error:
                    urlopen(url + "/unknown", timeout=3)
                self.assertEqual(error.exception.code, 404)
                error.exception.close()
                path.write_text("broken json", encoding="utf-8")
                with self.assertRaises(HTTPError) as error:
                    urlopen(url + "/", timeout=3)
                self.assertEqual(error.exception.code, 500)
                error.exception.close()


class CapstoneTests(unittest.TestCase):
    def test_persistent_lifecycle_and_unknown_id(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "requests.json"
            self.assertEqual(load_requests(path), [])
            self.assertEqual(add_request(path, " First "), 1)
            self.assertEqual(add_request(path, "Second"), 2)
            complete_request(path, 1)
            complete_request(path, 1)
            self.assertEqual(load_requests(path), [{"id": 1, "title": "First", "done": True},
                                                   {"id": 2, "title": "Second", "done": False}])
            before = path.read_bytes()
            with self.assertRaises(ValueError):
                complete_request(path, 999)
            self.assertEqual(path.read_bytes(), before)
            with self.assertRaises(ValueError):
                add_request(path, " ")

    def test_replace_failure_preserves_old_bytes(self):
        with TemporaryDirectory() as folder:
            path = Path(folder) / "requests.json"
            add_request(path, "Original")
            before = path.read_bytes()
            with patch("pathlib.Path.replace", side_effect=OSError("simulated failure")):
                with self.assertRaises(OSError):
                    save_requests(path, [])
            self.assertEqual(path.read_bytes(), before)
            self.assertEqual(list(Path(folder).glob(".requests-*.tmp")), [])

    def test_bad_records_survive_rejected_update(self):
        cases = ["{}", '[{"id":true,"title":"x","done":false}]',
                 '[{"id":1,"title":"x","done":false},{"id":1,"title":"y","done":true}]',
                 '[{"id":1,"title":"","done":false}]', '[{"id":1,"title":"x","done":"no"}]']
        for text in cases:
            with self.subTest(text=text), TemporaryDirectory() as folder:
                path = Path(folder) / "requests.json"
                path.write_text(text, encoding="utf-8")
                with self.assertRaises(ValueError):
                    add_request(path, "New")
                self.assertEqual(path.read_text(encoding="utf-8"), text)

    def test_cli_sequence_across_processes(self):
        environment = dict(os.environ, PYTHONPATH=str(ROOT), PYTHONIOENCODING="utf-8")
        commands = [(["add", "Check the workshop inventory"], "Added request #1\n"),
                    (["list"], "#1 [open] Check the workshop inventory\n"),
                    (["done", "1"], "Completed request #1\n"),
                    (["list"], "#1 [done] Check the workshop inventory\n")]
        with TemporaryDirectory() as folder:
            for arguments, expected in commands:
                result = subprocess.run([sys.executable, "-m", "examples.ch18.requests_cli", *arguments],
                                        cwd=folder, env=environment, capture_output=True,
                                        text=True, encoding="utf-8", timeout=10)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(result.stdout, expected)
