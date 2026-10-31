# Desktop project 2: request tracker

Use Python 3.11–3.14 with Tkinter. Follow [GUI setup](../../docs/gui-and-ai-setup.md).
From the repository root:

Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe -m examples.ch20.tracker --data requests.json
```

macOS/Linux:

```bash
./.venv/bin/python -m examples.ch20.tracker --data requests.json
```

Type a request title, then choose Add request or press Enter. Select a table
row and choose Mark selected complete. Refresh rereads the selected JSON file.
The same file works with Chapters 17 and 18. It is local single-writer storage;
do not run simultaneous writers. A missing file starts empty; malformed
existing data is reported and retained. Failed saves keep the typed title.

Tests invoke the real widgets, inspect the stored JSON and check rejected
empty input, failed saves, no selection and damaged storage.
