# Desktop project 1: focus timer

Python 3.11–3.14. Tkinter is required; no third-party Python packages.
First run your environment's Python with `-m tkinter`. A small demo window
should open. Close it before launching the project. See [GUI setup](../../docs/gui-and-ai-setup.md).

From the repository root:

| OS | First window | Timer |
|---|---|---|
| Windows PowerShell | `.\.venv\Scripts\python.exe -m examples.ch19.first_window` | `.\.venv\Scripts\python.exe -m examples.ch19.timer` |
| macOS/Linux | `./.venv/bin/python -m examples.ch19.first_window` | `./.venv/bin/python -m examples.ch19.timer` |

The first window's Try it button changes its message. The timer defaults to
25 minutes. `--seconds 90` gives a short practice run. Start begins or resumes,
Pause retains the remaining duration, and Reset restores the configured duration.
The display rounds remaining fractions up to the next second; it is a focus
aid, not a precision timekeeping instrument. Closing cancels scheduled callbacks.

Tests use actual Tk widgets and a controllable clock. On a Linux machine
without a desktop, run the suite through `xvfb-run -a`; CI does this explicitly.
No GUI test is silently skipped when Tk is unavailable.
