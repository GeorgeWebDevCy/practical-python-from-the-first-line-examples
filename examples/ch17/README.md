# Chapter 17 examples

Python 3.11–3.14, standard library only. Follow [setup for Windows, macOS and Linux](../../docs/setup.md) first. Commands below run from the repository root.

Runs until Ctrl+C. Open http://127.0.0.1:8766/ in your browser. Missing storage shows an empty board. HTTP is read-only and loopback-only; this teaching server is not for public deployment.

Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe -m examples.ch17.board --data requests.json
```

macOS/Linux:

```bash
./.venv/bin/python -m examples.ch17.board --data requests.json
```

Run tests from the root with the same interpreter:

```console
python -m unittest discover -s tests -v
```

Replace `python` with the explicit environment executable if it is not activated. Behaviour tests use temporary directories and local HTTP fixtures; no public API, credentials or third-party packages are required. See the book for assumptions and exercises.
