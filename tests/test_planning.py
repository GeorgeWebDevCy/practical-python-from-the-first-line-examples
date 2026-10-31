from io import BytesIO
import json
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from examples.ch21.planning import PlannerError, live_plan, offline_plan, validate_plan
from test_projects import serving
from http.server import BaseHTTPRequestHandler

TASK = {"title": "Draft a workshop checklist", "category": "planning"}


def envelope(tasks):
    return {"status": "completed", "output": [
        {"type": "reasoning", "summary": []},
        {"type": "message", "content": [{"type": "output_text", "text": json.dumps({"tasks": tasks})}]}]}


def transport_for(payload):
    body = json.dumps(payload).encode("utf-8")
    def send(request, timeout):
        return BytesIO(body)
    return send


class PlanningTests(unittest.TestCase):
    def test_offline_is_deterministic_without_network_or_credentials(self):
        with patch("examples.ch21.planning.build_opener", side_effect=AssertionError("Network used")):
            with patch.dict("os.environ", {}, clear=True):
                self.assertEqual(offline_plan("one goal"), offline_plan("another goal"))
                self.assertEqual(len(offline_plan("Prepare a workshop")), 3)
        for goal in ("", " " * 3, "x" * 601):
            with self.subTest(goal=goal[:10]), self.assertRaises(PlannerError):
                offline_plan(goal)

    def test_validation_rejects_structure_duplicates_and_unsafe_titles(self):
        self.assertEqual(validate_plan({"tasks": [TASK]}), [TASK])
        cases = [{}, {"tasks": []}, {"tasks": [TASK] * 6}, {"tasks": [TASK, TASK]},
                 {"tasks": [{"title": "x", "category": "other"}]},
                 {"tasks": [{"title": "bad\nline", "category": "coding"}]},
                 {"tasks": [{"title": "x" * 121, "category": "coding"}]},
                 {"tasks": [{"title": "x", "category": "coding", "execute": "anything"}]}]
        for payload in cases:
            with self.subTest(payload=payload), self.assertRaises(PlannerError):
                validate_plan(payload)

    def test_wire_contract_through_a_real_local_http_post(self):
        received = []
        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                body = self.rfile.read(int(self.headers["Content-Length"]))
                received.append((self.headers["Authorization"], json.loads(body)))
                response = json.dumps(envelope([TASK])).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(response)))
                self.end_headers()
                self.wfile.write(response)
            def log_message(self, format, *args):
                pass
        with serving(Handler) as url:
            def local_transport(request, timeout):
                self.assertEqual(request.full_url, "https://api.openai.com/v1/responses")
                self.assertEqual(request.get_method(), "POST")
                self.assertEqual(timeout, 20)
                return urlopen(Request(url, data=request.data, headers=dict(request.header_items()), method="POST"), timeout=timeout)
            result = live_plan("Prepare a workshop", api_key="fake-test-key", model="fixture-model", transport=local_transport)
        self.assertEqual(result, [TASK])
        header, payload = received[0]
        self.assertEqual(header, "Bearer fake-test-key")
        self.assertFalse(payload["store"])
        self.assertEqual(payload["input"], [{"role": "user", "content": "Prepare a workshop"}])
        self.assertTrue(payload["text"]["format"]["strict"])
        self.assertEqual(payload["text"]["format"]["type"], "json_schema")

    def test_incomplete_refusal_and_malformed_messages(self):
        cases = [{"status": "incomplete", "output": []},
                 {"status": "completed", "output": [{"type": "message", "content": [{"type": "refusal", "refusal": "No"}]}]},
                 {"status": "completed", "output": []},
                 {"status": "completed", "output": "bad"},
                 {"status": "completed", "output": [{"type": "message", "content": [{"type": "output_text", "text": "broken"}]}]}]
        for payload in cases:
            with self.subTest(payload=payload), self.assertRaises(PlannerError):
                live_plan("Goal", api_key="fake", model="fixture", transport=transport_for(payload))

    def test_credentials_network_errors_and_response_limit(self):
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(PlannerError):
                live_plan("Goal")
        with self.assertRaises(PlannerError) as error:
            live_plan("Goal", api_key="secret\nvalue", model="fixture")
        self.assertNotIn("secret", str(error.exception))
        for code in (401, 429, 500, 302):
            def failed(request, timeout):
                raise HTTPError(request.full_url, code, "failure", {}, BytesIO(b"private body fake-key"))
            with self.subTest(code=code), self.assertRaises(PlannerError) as error:
                live_plan("Goal", api_key="fake-key", model="fixture", transport=failed)
            self.assertNotIn("fake-key", str(error.exception))
            self.assertNotIn("private body", str(error.exception))
        def timeout(request, timeout):
            raise TimeoutError("private diagnostic")
        with self.assertRaises(PlannerError) as error:
            live_plan("Goal", api_key="fake", model="fixture", transport=timeout)
        self.assertNotIn("private", str(error.exception))
        with self.assertRaises(PlannerError):
            live_plan("Goal", api_key="fake", model="fixture", transport=lambda r, timeout: BytesIO(b"x" * 131073))
