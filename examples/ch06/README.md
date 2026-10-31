# Chapter 6 examples

Python 3.11–3.14, standard library only. Follow [setup for Windows, macOS and Linux](../../docs/setup.md) first. Commands below run from the repository root.

Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe examples/ch06/weekly.py
```

macOS/Linux:

```bash
./.venv/bin/python examples/ch06/weekly.py
```

Expected captured output:

```text
Session 1: 15 minutes
Session 2: 20 minutes
Session 3: 10 minutes
Weekly total: 45 minutes
Countdown: 3
Countdown: 2
Countdown: 1
```

Run tests from the root with the same interpreter:

```console
python -m unittest discover -s tests -v
```

Replace `python` with the explicit environment executable if it is not activated. Behaviour tests use temporary directories and local HTTP fixtures; no public API, credentials or third-party packages are required. See the book for assumptions and exercises.
