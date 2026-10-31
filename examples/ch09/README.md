# Chapter 9 examples

Python 3.11–3.14, standard library only. Follow [setup for Windows, macOS and Linux](../../docs/setup.md) first. Commands below run from the repository root.

Creates `practice-plan.json` only if absent, then reads the existing file on later runs. Use a disposable working copy for experiments.

Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe examples/ch09/plan_store.py
```

macOS/Linux:

```bash
./.venv/bin/python examples/ch09/plan_store.py
```

Expected captured output:

```text
Stored sessions: 1
Total minutes: 25
```

Run tests from the root with the same interpreter:

```console
python -m unittest discover -s tests -v
```

Replace `python` with the explicit environment executable if it is not activated. Behaviour tests use temporary directories and local HTTP fixtures; no public API, credentials or third-party packages are required. See the book for assumptions and exercises.
