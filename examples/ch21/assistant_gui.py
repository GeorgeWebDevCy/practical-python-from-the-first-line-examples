"""Review task suggestions before adding them to the local desktop tracker."""

import argparse
from pathlib import Path
from queue import Empty, Queue
from threading import Thread
import tkinter as tk
from tkinter import ttk

from examples.ch20.tracker import RequestTracker
from examples.ch21.planning import (
    PlannerError,
    clean_goal,
    live_plan,
    offline_plan,
    validate_plan,
)


class PlanningAssistant(ttk.Frame):
    def __init__(
        self, master, data_path, *, provider=offline_plan, live=False
    ):
        super().__init__(master, padding=18)
        self.provider, self.live = provider, live
        self.goal = tk.StringVar(master)
        self.status = tk.StringVar(
            master, "Enter a goal, request suggestions, then review them."
        )
        self.consent = tk.BooleanVar(master, False)
        self.results = Queue()
        self.tasks = []
        self.generation = 0
        self.busy = self.closed = False
        self.job = self.worker = None
        self.columnconfigure(0, weight=1)
        self.rowconfigure(6, weight=1)
        ttk.Label(
            self,
            text="Plan a small next step",
            font=("TkDefaultFont", 18, "bold"),
        ).grid(sticky="w")
        mode = (
            "Live OpenAI API: requests may incur charges"
            if live
            else "Offline demonstration: fixed suggestions, no network"
        )
        ttk.Label(self, text=mode).grid(row=1, sticky="w", pady=(4, 12))
        goal_frame = ttk.Frame(self)
        goal_frame.grid(row=2, sticky="ew")
        goal_frame.columnconfigure(1, weight=1)
        ttk.Label(goal_frame, text="Goal:").grid(
            row=0, column=0, padx=(0, 8)
        )
        self.goal_entry = ttk.Entry(
            goal_frame, textvariable=self.goal, width=55
        )
        self.goal_entry.grid(row=0, column=1, sticky="ew")
        self.suggest_button = ttk.Button(
            goal_frame, text="Suggest steps", command=self.suggest
        )
        self.suggest_button.grid(row=0, column=2, padx=(8, 0))
        if live:
            ttk.Checkbutton(
                self,
                text="Send only this goal to the configured service",
                variable=self.consent,
            ).grid(row=3, sticky="w", pady=8)
        review = ttk.Frame(self)
        review.grid(row=4, sticky="ew", pady=10)
        review.columnconfigure(0, weight=1)
        self.suggestions = ttk.Treeview(
            review,
            columns=("category", "title"),
            show="headings",
            selectmode="browse",
            height=4,
        )
        self.suggestions.heading("category", text="Suggested category")
        self.suggestions.heading(
            "title", text="Suggested task — review before adding"
        )
        self.suggestions.column("category", width=135, stretch=False)
        self.suggestions.column("title", width=530)
        self.suggestions.grid(row=0, column=0, sticky="ew")
        actions = ttk.Frame(review)
        actions.grid(row=1, column=0, sticky="w", pady=8)
        self.accept_button = ttk.Button(
            actions, text="Add selected suggestion", command=self.accept
        )
        self.accept_button.grid(row=0, column=0)
        ttk.Label(self, textvariable=self.status, wraplength=780).grid(
            row=5, sticky="w", pady=(0, 12)
        )
        self.tracker = RequestTracker(self, data_path)
        self.tracker.grid(row=6, sticky="nsew")
        self.accept_button.state(["disabled"])

    def suggest(self):
        if self.busy or self.closed:
            return
        try:
            goal = clean_goal(self.goal.get())
            if self.live and not self.consent.get():
                raise PlannerError(
                    "Review the goal and confirm sending it before using live mode."
                )
        except PlannerError as error:
            self.status.set(str(error))
            return
        self.generation += 1
        generation = self.generation
        self.busy = True
        self.tasks = []
        self.suggestions.delete(*self.suggestions.get_children())
        self.suggest_button.state(["disabled"])
        self.goal_entry.state(["disabled"])
        self.accept_button.state(["disabled"])
        self.status.set(
            "Preparing suggestions. Your local requests have not changed."
        )

        def work():
            try:
                tasks = validate_plan({"tasks": self.provider(goal)})
                result = (generation, tasks, None)
            except PlannerError as error:
                result = (generation, None, str(error))
            except Exception:
                result = (
                    generation,
                    None,
                    "Suggestion request failed. No local requests were changed.",
                )
            self.results.put(result)

        self.worker = Thread(target=work, daemon=True)
        self.worker.start()
        self.job = self.after(50, self.poll)

    def poll(self):
        if self.job is not None:
            self.after_cancel(self.job)
            self.job = None
        if self.closed:
            return
        try:
            generation, tasks, error = self.results.get_nowait()
        except Empty:
            if self.busy:
                self.job = self.after(50, self.poll)
            return
        if generation != self.generation:
            return
        self.busy = False
        self.suggest_button.state(["!disabled"])
        self.goal_entry.state(["!disabled"])
        if error:
            self.status.set(error)
            return
        self.tasks = tasks
        for index, task in enumerate(tasks):
            self.suggestions.insert(
                "",
                "end",
                iid=str(index),
                values=(task["category"], task["title"]),
            )
        self.accept_button.state(["!disabled"])
        self.status.set(
            "Review these suggestions. Select one to add; "
            "nothing is saved automatically."
        )

    def accept(self):
        if self.busy or self.closed:
            return False
        selected = self.suggestions.selection()
        if not selected:
            self.status.set("Select a suggestion first.")
            return False
        index = int(selected[0])
        self.tracker.title_text.set(self.tasks[index]["title"])
        if not self.tracker.add():
            self.status.set(
                "The selected suggestion could not be saved. Check the tracker message."
            )
            return False
        self.suggestions.delete(selected[0])
        if not self.suggestions.get_children():
            self.accept_button.state(["disabled"])
        self.status.set(
            "Added the selected title to local requests. "
            "Other suggestions are still unsaved."
        )
        return True

    def close(self):
        self.closed = True
        self.generation += 1
        if self.job is not None:
            self.after_cancel(self.job)
            self.job = None
        self.winfo_toplevel().destroy()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, default=Path("requests.json"))
    parser.add_argument(
        "--live",
        action="store_true",
        help="Enable optional billable OpenAI requests",
    )
    args = parser.parse_args()
    root = tk.Tk()
    root.title("Python Book | Task planning assistant")
    root.minsize(880, 740)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    app = PlanningAssistant(
        root,
        args.data,
        provider=live_plan if args.live else offline_plan,
        live=args.live,
    )
    app.grid(sticky="nsew")
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()


if __name__ == "__main__":
    main()
