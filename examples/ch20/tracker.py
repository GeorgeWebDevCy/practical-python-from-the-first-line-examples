"""A desktop interface for the existing local request store."""

import argparse
from pathlib import Path
import tkinter as tk
from tkinter import ttk

from examples.ch17.board import load_requests
from examples.ch18.requests_cli import add_request, complete_request


class RequestTracker(ttk.Frame):
    def __init__(self, master, data_path):
        super().__init__(master, padding=18)
        self.data_path = Path(data_path)
        self.title_text = tk.StringVar(master)
        self.status = tk.StringVar(master)
        self.summary = tk.StringVar(master)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)
        ttk.Label(
            self,
            text="My request tracker",
            font=("TkDefaultFont", 18, "bold"),
        ).grid(sticky="w")
        ttk.Label(
            self,
            text="Saved on this computer. Refresh after edits from another interface.",
        ).grid(row=1, sticky="w", pady=8)
        editor = ttk.Frame(self)
        editor.grid(row=2, sticky="ew", pady=(0, 12))
        editor.columnconfigure(1, weight=1)
        ttk.Label(editor, text="Request title:").grid(
            row=0, column=0, padx=(0, 8)
        )
        self.entry = ttk.Entry(
            editor, textvariable=self.title_text, width=45
        )
        self.entry.grid(row=0, column=1, sticky="ew")
        self.entry.bind("<Return>", lambda event: self.add())
        self.add_button = ttk.Button(
            editor, text="Add request", command=self.add
        )
        self.add_button.grid(row=0, column=2, padx=(8, 0))
        table = ttk.Frame(self)
        table.grid(row=3, sticky="nsew")
        table.columnconfigure(0, weight=1)
        table.rowconfigure(0, weight=1)
        self.tree = ttk.Treeview(
            table,
            columns=("id", "status", "title"),
            show="headings",
            selectmode="browse",
            height=9,
        )
        for name, label, width in (
            ("id", "ID", 50),
            ("status", "Status", 90),
            ("title", "Request", 400),
        ):
            self.tree.heading(name, text=label)
            self.tree.column(name, width=width, stretch=name == "title")
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(
            table, orient="vertical", command=self.tree.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)
        actions = ttk.Frame(self)
        actions.grid(row=4, sticky="ew", pady=12)
        self.complete_button = ttk.Button(
            actions, text="Mark selected complete", command=self.complete
        )
        self.complete_button.grid(row=0, column=0)
        ttk.Button(actions, text="Refresh", command=self.refresh).grid(
            row=0, column=1, padx=8
        )
        ttk.Label(actions, textvariable=self.summary).grid(
            row=0, column=2, padx=12
        )
        ttk.Label(self, textvariable=self.status, wraplength=690).grid(
            row=5, sticky="w"
        )
        self.refresh()

    def refresh(self):
        try:
            records = load_requests(self.data_path)
        except (OSError, ValueError):
            self.status.set(
                "Could not load requests. Check the JSON file; "
                "existing data was not replaced."
            )
            return False
        selected = self.tree.selection()
        self.tree.delete(*self.tree.get_children())
        for row in records:
            self.tree.insert(
                "",
                "end",
                iid=str(row["id"]),
                values=(
                    row["id"],
                    "done" if row["done"] else "open",
                    row["title"],
                ),
            )
        if selected and self.tree.exists(selected[0]):
            self.tree.selection_set(selected[0])
        self.summary.set(
            f"{sum(not row['done'] for row in records)} open / {len(records)} total"
        )
        self.status.set(
            "Ready. Add a request or select one to mark complete."
        )
        return True

    def add(self):
        try:
            identifier = add_request(self.data_path, self.title_text.get())
        except (OSError, ValueError) as error:
            self.status.set(f"Could not add request: {error}")
            return False
        self.title_text.set("")
        self.refresh()
        self.tree.selection_set(str(identifier))
        self.tree.see(str(identifier))
        self.status.set(f"Added request #{identifier}.")
        self.entry.focus_set()
        return True

    def complete(self):
        selected = self.tree.selection()
        if not selected:
            self.status.set("Select a request first.")
            return False
        try:
            identifier = int(selected[0])
            complete_request(self.data_path, identifier)
        except (OSError, ValueError) as error:
            self.status.set(f"Could not complete request: {error}")
            return False
        self.refresh()
        self.status.set(f"Completed request #{identifier}.")
        return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("requests.json"))
    args = parser.parse_args()
    root = tk.Tk()
    root.title("Python Book | Desktop request tracker")
    root.minsize(760, 480)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    RequestTracker(root, args.data).grid(sticky="nsew")
    root.mainloop()


if __name__ == "__main__":
    main()
