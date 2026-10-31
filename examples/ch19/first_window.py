"""Your first small window: a label, a button and a callback."""

import tkinter as tk
from tkinter import ttk


def build_window(root):
    root.title("Practical Python | First window")
    frame = ttk.Frame(root, padding=24)
    frame.grid()
    message = tk.StringVar(root, "Ready for a small experiment.")
    ttk.Label(frame, textvariable=message).grid(row=0, column=0, pady=12)

    def change_message():
        message.set("You pressed the button.")

    button = ttk.Button(frame, text="Try it", command=change_message)
    button.grid(row=1, column=0, pady=12)
    return message, button


if __name__ == "__main__":
    root = tk.Tk()
    build_window(root)
    root.mainloop()
