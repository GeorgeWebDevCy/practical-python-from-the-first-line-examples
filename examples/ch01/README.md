# Chapter 1 — Run a saved program

No additional dependencies. Use Python 3.11–3.14 and follow the
[Windows, macOS and Linux setup guide](../../docs/setup.md) first.
Run from the repository root.

Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe examples/ch01/practice.py
```

macOS/Linux:

```bash
./.venv/bin/python examples/ch01/practice.py
```

Expected output:

```text
Today's practice
Reading minutes: 10
Total minutes: 15
```

`my_practice.py` is a possible exercise solution. Run it with the same command,
replacing the final filename. It prints:

```text
Learning to organise my files
Reading minutes: 12
Total minutes: 19
```

Use a separate scratch file for experiments, or restore these files before
running tests. Run all behaviour tests with your environment's Python:

```console
python -m unittest discover -s tests -v
```

Tests check both complete outputs and compile a deliberately broken snippet to
verify a syntax error. Expected error wording is not tied to one Python version.
