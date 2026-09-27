import os
import tkinter as tk
from tkinter import messagebox
from pathlib import Path

APP_NAME = "HATERMINAL"
VERSION = "1.0"


class Haterminal:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_NAME)
        self.root.geometry("900x550")
        self.root.configure(bg="black")

        self.output = tk.Text(
            self.root,
            bg="black",
            fg="#00ff66",
            font=("Consolas", 11),
            borderwidth=0,
            highlightthickness=0,
            state="disabled"
        )
        self.output.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(10, 0)
        )

        self.entry = tk.Entry(
            self.root,
            bg="black",
            fg="#00ff66",
            insertbackground="#00ff66",
            font=("Consolas", 11),
            borderwidth=0,
            highlightthickness=0
        )
        self.entry.pack(
            fill="x",
            padx=10,
            pady=10
        )

        self.entry.bind("<Return>", self.execute)

        # Pencere açılır açılmaz yazı alanına odaklan
        self.root.after(100, self.focus_entry)

        # Terminale tıklanınca tekrar yazı alanına odaklan
        self.root.bind("<Button-1>", self.mouse_click)

        self.current_directory = Path.cwd()

        self.write("HATERMINAL v1.0")
        self.write("Safe Terminal Mode")
        self.write("Type HELP for commands.")
        self.write("")

    def focus_entry(self):
        self.root.lift()
        self.root.focus_force()
        self.entry.focus_set()

    def mouse_click(self, event=None):
        self.entry.focus_set()

    def write(self, text):
        self.output.config(state="normal")
        self.output.insert("end", text + "\n")
        self.output.see("end")
        self.output.config(state="disabled")

    def translate_path(self, path):
        path = path.strip()

        if path.startswith("/*/"):
            path = path[3:]

        return Path(path.replace("/", os.sep))

    def get_message(self, command):
        if ":" not in command:
            return ""

        return command.split(":", 1)[1].strip().strip('"')

    def execute(self, event=None):
        command = self.entry.get().strip()

        if not command:
            return "break"

        self.entry.delete(0, "end")
        self.write("HATERMINAL-> " + command)

        lower = command.lower()

        if lower == "exit":
            self.root.destroy()
            return "break"

        if lower == "clear":
            self.output.config(state="normal")
            self.output.delete("1.0", "end")
            self.output.config(state="disabled")
            self.entry.focus_set()
            return "break"

        if lower == "help":
            self.write("")
            self.write("HATERMINAL COMMANDS")
            self.write("-------------------")
            self.write("")
            self.write("HELP")
            self.write("CLEAR")
            self.write("ABOUT")
            self.write("PWD")
            self.write("")
            self.write("OPEN <file>:")
            self.write("OPENAT /*/<path>: <file>")
            self.write("")
            self.write('OPEN-POPUP: "message"')
            self.write('OPENAT-POPUP /*/<path>: "message"')
            self.write("")
            self.write('OPEN-ERROR: "message"')
            self.write('OPENAT-ERROR /*/<path>: "message"')
            self.write("")
            self.write('OPEN-INFORMATION: "message"')
            self.write('OPENAT-INFORMATION /*/<path>: "message"')
            self.write("")
            self.write("EXIT")
            self.write("")
            self.entry.focus_set()
            return "break"

        if lower == "about":
            self.write("")
            self.write("HATERMINAL")
            self.write("Version: " + VERSION)
            self.write("Safe Terminal")
            self.write("")
            self.entry.focus_set()
            return "break"

        if lower == "pwd":
            self.write(str(self.current_directory))
            self.write("")
            self.entry.focus_set()
            return "break"

        if lower.startswith("open-popup:"):
            messagebox.showinfo(
                "HATERMINAL",
                self.get_message(command)
            )
            self.entry.focus_set()
            return "break"

        if lower.startswith("openat-popup "):
            self.openat_window(command, "popup")
            self.entry.focus_set()
            return "break"

        if lower.startswith("open-error:"):
            messagebox.showerror(
                "HATERMINAL ERROR",
                self.get_message(command)
            )
            self.entry.focus_set()
            return "break"

        if lower.startswith("openat-error "):
            self.openat_window(command, "error")
            self.entry.focus_set()
            return "break"

        if lower.startswith("open-information:"):
            messagebox.showinfo(
                "HATERMINAL INFORMATION",
                self.get_message(command)
            )
            self.entry.focus_set()
            return "break"

        if lower.startswith("openat-information "):
            self.openat_window(command, "information")
            self.entry.focus_set()
            return "break"

        if lower.startswith("openat "):
            self.openat_file(command)
            self.entry.focus_set()
            return "break"

        if lower.startswith("open "):
            self.open_file(command)
            self.entry.focus_set()
            return "break"

        self.write("Unknown command.")
        self.write("Type HELP for available commands.")
        self.write("")

        self.entry.focus_set()
        return "break"

    def openat_window(self, command, window_type):
        try:
            before, message = command.split(":", 1)
            parts = before.split(" ", 1)

            if len(parts) != 2:
                self.write("Invalid OPENAT syntax.")
                return

            path = self.translate_path(parts[1])
            message = message.strip().strip('"')

            if not path.exists():
                self.write("Location not found:")
                self.write(str(path))
                self.write("")
                return

            if window_type == "error":
                messagebox.showerror(
                    "HATERMINAL ERROR",
                    message
                )
            elif window_type == "information":
                messagebox.showinfo(
                    "HATERMINAL INFORMATION",
                    message
                )
            else:
                messagebox.showinfo(
                    "HATERMINAL",
                    message
                )

        except Exception as e:
            self.write("OPENAT error: " + str(e))
            self.write("")

    def open_file(self, command):
        try:
            name = command[5:].strip()

            if name.endswith(":"):
                name = name[:-1].strip()

            self.show_file(
                self.current_directory / name
            )

        except Exception as e:
            self.write("OPEN error: " + str(e))
            self.write("")

    def openat_file(self, command):
        try:
            before, filename = command.split(":", 1)

            path_text = before[len("openat "):].strip()
            path = self.translate_path(path_text)

            filename = filename.strip().strip('"')

            self.show_file(path / filename)

        except Exception as e:
            self.write("OPENAT error: " + str(e))
            self.write("")

    def show_file(self, path):
        if not path.exists():
            self.write("File not found:")
            self.write(str(path))
            self.write("")
            return

        if not path.is_file():
            self.write("Not a file:")
            self.write(str(path))
            self.write("")
            return

        try:
            content = path.read_text(
                encoding="utf-8",
                errors="replace"
            )
        except Exception as e:
            self.write("Cannot read file:")
            self.write(str(e))
            self.write("")
            return

        self.write("FILE: " + str(path))
        self.write("-" * 60)

        if content:
            for line in content.splitlines():
                self.write(line)
        else:
            self.write("[empty file]")

        self.write("-" * 60)
        self.write("")


if __name__ == "__main__":
    app = Haterminal()
    app.root.mainloop()
