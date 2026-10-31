# Chapter 16 examples

Python 3.11–3.14, standard library only. Follow [setup for Windows, macOS and Linux](../../docs/setup.md) first. Commands below run from the repository root.

First run `python -m examples.toolkit.fixture` in another terminal with the same environment selected. It serves controlled loopback data. Stop it with Ctrl+C afterward.

Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe examples/ch16/fetch.py http://127.0.0.1:8765/sessions
```

macOS/Linux:

```bash
./.venv/bin/python examples/ch16/fetch.py http://127.0.0.1:8765/sessions
```

Expected captured output:

```text
Sessions received: 2
Total minutes: 45
```

Run tests from the root with the same interpreter:

```console
python -m unittest discover -s tests -v
```

Replace `python` with the explicit environment executable if it is not activated. Behaviour tests use temporary directories and local HTTP fixtures; no public API, credentials or third-party packages are required. See the book for assumptions and exercises.
