# Chapter 18 examples

Python 3.11–3.14, standard library only. Follow [setup for Windows, macOS and Linux](../../docs/setup.md) first. Commands below run from the repository root.

For the displayed ID, start with no `requests.json`. Then use the same module with `list`, `done 1`, and `list` to see persistence. Run the Chapter 17 board with the same data file to view it. Only one writer at a time is supported.

Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe -m examples.ch18.requests_cli --data requests.json add "Check the workshop inventory"
```

macOS/Linux:

```bash
./.venv/bin/python -m examples.ch18.requests_cli --data requests.json add "Check the workshop inventory"
```

Expected captured output:

```text
Added request #1
```

Run tests from the root with the same interpreter:

```console
python -m unittest discover -s tests -v
```

Replace `python` with the explicit environment executable if it is not activated. Behaviour tests use temporary directories and local HTTP fixtures; no public API, credentials or third-party packages are required. See the book for assumptions and exercises.
