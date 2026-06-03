import threading
import tkinter as tk
from tkinter import ttk

from scanner_engine import scan_target


def start_scan():

    target = target_entry.get()

    if not target:

        results_box.delete("1.0", tk.END)

        results_box.insert(
            tk.END,
            "Please enter a target."
        )

        return

    result = scan_target(
    target,
    scan_mode.get()
)

    results_box.delete("1.0", tk.END)

    for line in result:

        results_box.insert(
            tk.END,
            line + "\n"
        )


root = tk.Tk()

root.title("Advanced Port Scanner")
root.geometry("700x500")


title_label = tk.Label(
    root,
    text="Advanced Port Scanner",
    font=("Arial", 18, "bold")
)
title_label.pack(pady=10)


target_label = tk.Label(
    root,
    text="Target IP or Hostname:"
)
target_label.pack()


target_entry = tk.Entry(
    root,
    width=50
)
target_entry.pack(pady=5)


scan_mode = tk.StringVar()
scan_mode.set("Quick")


ttk.Radiobutton(
    root,
    text="Quick Scan",
    variable=scan_mode,
    value="Quick"
).pack()


ttk.Radiobutton(
    root,
    text="Standard Scan",
    variable=scan_mode,
    value="Standard"
).pack()


ttk.Radiobutton(
    root,
    text="Full Scan",
    variable=scan_mode,
    value="Full"
).pack()


import threading

start_button = tk.Button(
    root,
    text="Start Scan",
    command=lambda: threading.Thread(
        target=start_scan,
        daemon=True
    ).start(),
    width=20
)
start_button.pack(pady=10)


results_label = tk.Label(
    root,
    text="Results"
)
results_label.pack()


results_box = tk.Text(
    root,
    height=15,
    width=80
)
results_box.pack(pady=10)


root.mainloop()
