# Chapter 14 examples

Python 3.11–3.14, standard library only. Follow [setup for Windows, macOS and Linux](../../docs/setup.md) first. Commands below run from the repository root.

Creates a new `costs.svg` in the working directory. Existing output is rejected. Open the SVG in a browser.

Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe examples/ch14/chart.py
```

macOS/Linux:

```bash
./.venv/bin/python examples/ch14/chart.py
```

Expected captured output:

```text
Created costs.svg
```

Run tests from the root with the same interpreter:

```console
python -m unittest discover -s tests -v
```

Replace `python` with the explicit environment executable if it is not activated. Behaviour tests use temporary directories and local HTTP fixtures; no public API, credentials or third-party packages are required. See the book for assumptions and exercises.
