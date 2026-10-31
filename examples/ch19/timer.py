"""A small desktop timer. Run: python -m examples.ch19.timer."""

import argparse
import math
import time
import tkinter as tk
from tkinter import ttk


class FocusTimer(ttk.Frame):
    def __init__(self, master, seconds=1500, clock=time.monotonic):
        if type(seconds) is not int or seconds <= 0:
            raise ValueError(
                "Duration must be a positive whole number of seconds"
            )
        super().__init__(master, padding=24)
        self.clock = clock
        self.duration = self.remaining = seconds
        self.deadline = None
        self.job = None
        self.running = False
        self.display = tk.StringVar(master)
        self.status = tk.StringVar(master, "Ready when you are.")
        self.grid(sticky="nsew")
        self.columnconfigure(0, weight=1)
        ttk.Label(
            self, text="Focus timer", font=("TkDefaultFont", 20, "bold")
        ).grid(pady=(0, 12))
        ttk.Label(
            self, textvariable=self.display, font=("TkDefaultFont", 42)
        ).grid(pady=8)
        buttons = ttk.Frame(self)
        buttons.grid(pady=16)
        self.start_button = ttk.Button(
            buttons, text="Start", command=self.start
        )
        self.pause_button = ttk.Button(
            buttons, text="Pause", command=self.pause
        )
        self.reset_button = ttk.Button(
            buttons, text="Reset", command=self.reset
        )
        for column, button in enumerate(
            (self.start_button, self.pause_button, self.reset_button)
        ):
            button.grid(row=0, column=column, padx=5)
        ttk.Label(self, textvariable=self.status, wraplength=430).grid(
            pady=8
        )
        self._show()

    def _show(self):
        minutes, seconds = divmod(math.ceil(self.remaining), 60)
        self.display.set(f"{minutes:02d}:{seconds:02d}")
        self.start_button.state(
            ["disabled"]
            if self.running or not self.remaining
            else ["!disabled"]
        )
        self.pause_button.state(
            ["!disabled"] if self.running else ["disabled"]
        )

    def _cancel(self):
        if self.job is not None:
            self.after_cancel(self.job)
            self.job = None

    def tick(self):
        self._cancel()
        if not self.running:
            return
        self.remaining = max(0, self.deadline - self.clock())
        if self.remaining == 0:
            self.running = False
            self.status.set("Session complete. Reset to begin another.")
        else:
            self.job = self.after(200, self.tick)
        self._show()

    def start(self):
        if self.running or self.remaining == 0:
            return
        self.deadline = self.clock() + self.remaining
        self.running = True
        self.status.set("Focus on one small task.")
        self.tick()

    def pause(self):
        if self.running:
            self.tick()
            self.running = False
            self._cancel()
            if self.remaining:
                self.status.set("Paused. Start resumes the remaining time.")
            self._show()

    def reset(self):
        self._cancel()
        self.running = False
        self.remaining = self.duration
        self.status.set("Ready when you are.")
        self._show()

    def close(self):
        self._cancel()
        self.winfo_toplevel().destroy()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seconds", type=int, default=1500)
    args = parser.parse_args()
    if args.seconds <= 0:
        parser.error("--seconds must be positive")
    root = tk.Tk()
    root.title("Practical Python | Focus timer")
    root.minsize(520, 320)
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    timer = FocusTimer(root, args.seconds)
    root.protocol("WM_DELETE_WINDOW", timer.close)
    root.mainloop()


if __name__ == "__main__":
    main()
