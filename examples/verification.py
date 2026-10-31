"""Run documented commands in temporary directories with a local HTTP fixture."""

from contextlib import contextmanager
from http.server import ThreadingHTTPServer
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
from threading import Thread
from examples.toolkit.fixture import FixtureHandler

ROOT = Path(__file__).resolve().parents[1]


@contextmanager
def local_fixture():
    with ThreadingHTTPServer(("127.0.0.1", 0), FixtureHandler) as server:
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            yield f"http://127.0.0.1:{server.server_port}"
        finally:
            server.shutdown()
            thread.join(timeout=5)


def run_case(case):
    if case.get("test_only"):
        return
    with TemporaryDirectory() as folder, local_fixture() as fixture:
        for name, text in case.get("files", {}).items():
            path = Path(folder) / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        command = [sys.executable]
        command += (
            ["-m", case["module"]]
            if "module" in case
            else [str(ROOT / case["script"])]
        )
        command += [
            item.replace("{fixture}", fixture)
            for item in case.get("argv", [])
        ]
        environment = dict(
            os.environ, PYTHONPATH=str(ROOT), PYTHONIOENCODING="utf-8"
        )
        result = subprocess.run(
            command,
            cwd=folder,
            env=environment,
            input=case.get("stdin", ""),
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=15,
        )
        if (
            result.returncode
            or result.stdout != case["stdout"]
            or result.stderr
        ):
            raise AssertionError(
                f"Unexpected result for {case['script']}: {result!r}"
            )


if __name__ == "__main__":
    cases = json.loads(
        (ROOT / "examples/cases.json").read_text(encoding="utf-8")
    )["cases"]
    for case in cases:
        run_case(case)
        print(
            f"Chapter {case['chapter']}: {'integration suite required' if case.get('test_only') else 'command verified'}"
        )
