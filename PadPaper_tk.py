# PadPaper Editor Tkinter 2.0 - the OpenSource Text editor system
# Copyright (C) 2024 Proyecto Facilitar el Software Libre en el Ecuador

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; version 1
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330,
# Boston, MA  02111-1307, USA.

# Modificaciones realizadas por [Washington Indacochea Delgado] en [2024]
# Basado en el código original de [Gerardo Orellana]
#
# Créditos:
# - [Washington Indacochea Delgado]: Modificaciones y mejoras (2024)
#   Proyecto Facilitar el Software Libre en el Ecuador
#   EMail: wachin.id@gmail.com
#
# - [Gerardo Orellana]: Código original (2003)
#   Pro Soft
#   EMail: hello@goaccess.io

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, colorchooser, font
import os
import subprocess

class ModernTextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Text Editor")
        self.root.geometry("1000x600")

        self.filename = None
        self.current_font = ("Courier", 12)
        self.current_theme = "light"

        self.create_widgets()
        self.create_menu()
        self.apply_theme()

    def create_widgets(self):
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.text_area = tk.Text(self.main_frame, wrap=tk.WORD, undo=True, font=self.current_font)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.text_area)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_area.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_area.yview)

        self.status_bar = ttk.Label(self.root, text="Ready", anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Ctrl+Q")

        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.text_area.edit_undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.text_area.edit_redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut_text, accelerator="Ctrl+X")
        edit_menu.add_command(label="Copy", command=self.copy_text, accelerator="Ctrl+C")
        edit_menu.add_command(label="Paste", command=self.paste_text, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Find", command=self.find_text, accelerator="Ctrl+F")
        edit_menu.add_command(label="Replace", command=self.replace_text, accelerator="Ctrl+H")

        format_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Format", menu=format_menu)
        format_menu.add_command(label="Font", command=self.change_font)
        format_menu.add_command(label="Color", command=self.change_color)

        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Toggle Theme", command=self.toggle_theme)

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

        self.root.bind("<Control-n>", lambda event: self.new_file())
        self.root.bind("<Control-o>", lambda event: self.open_file())
        self.root.bind("<Control-s>", lambda event: self.save_file())
        self.root.bind("<Control-S>", lambda event: self.save_as_file())
        self.root.bind("<Control-q>", lambda event: self.root.quit())
        self.root.bind("<Control-f>", lambda event: self.find_text())
        self.root.bind("<Control-h>", lambda event: self.replace_text())

    def new_file(self):
        self.text_area.delete(1.0, tk.END)
        self.filename = None
        self.status_bar.config(text="New File")

    def open_file(self):
        file = filedialog.askopenfile(defaultextension=".txt",
                                      filetypes=[("All Files", "*.*"),
                                                 ("Text Documents", "*.txt")])
        if file:
            self.filename = file.name
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(1.0, file.read())
            file.close()
            self.status_bar.config(text=f"Opened: {self.filename}")

    def save_file(self):
        if self.filename:
            try:
                content = self.text_area.get(1.0, tk.END)
                with open(self.filename, "w") as file:
                    file.write(content)
                self.status_bar.config(text=f"Saved: {self.filename}")
            except Exception as e:
                messagebox.showerror("Error", f"Unable to save file: {str(e)}")
        else:
            self.save_as_file()

    def save_as_file(self):
        file = filedialog.asksaveasfile(defaultextension=".txt",
                                        filetypes=[("All Files", "*.*"),
                                                   ("Text Documents", "*.txt")])
        if file:
            self.filename = file.name
            content = self.text_area.get(1.0, tk.END)
            file.write(content)
            file.close()
            self.status_bar.config(text=f"Saved: {self.filename}")

    def cut_text(self):
        self.text_area.event_generate("<<Cut>>")

    def copy_text(self):
        self.text_area.event_generate("<<Copy>>")

    def paste_text(self):
        self.text_area.event_generate("<<Paste>>")

    def find_text(self):
        search_toplevel = tk.Toplevel(self.root)
        search_toplevel.title("Find Text")
        search_toplevel.transient(self.root)
        search_toplevel.resizable(False, False)

        ttk.Label(search_toplevel, text="Find:").grid(row=0, column=0, sticky="e")
        search_entry = ttk.Entry(search_toplevel, width=30)
        search_entry.grid(row=0, column=1, padx=2, pady=2, sticky="we")
        search_entry.focus_set()

        def do_find():
            self.text_area.tag_remove("match", "1.0", tk.END)
            count = 0
            search_string = search_entry.get()
            if search_string:
                pos = "1.0"
                while True:
                    pos = self.text_area.search(search_string, pos, nocase=1, stopindex=tk.END)
                    if not pos:
                        break
                    end = f"{pos}+{len(search_string)}c"
                    self.text_area.tag_add("match", pos, end)
                    count += 1
                    pos = end
                self.text_area.tag_config("match", foreground="red", background="yellow")
            self.status_bar.config(text=f"{count} matches found")

        ttk.Button(search_toplevel, text="Find All", command=do_find).grid(row=0, column=2, sticky="e" + "w", padx=2, pady=2)

    def replace_text(self):
        replace_toplevel = tk.Toplevel(self.root)
        replace_toplevel.title("Replace Text")
        replace_toplevel.transient(self.root)
        replace_toplevel.resizable(False, False)

        ttk.Label(replace_toplevel, text="Find:").grid(row=0, column=0, sticky="e")
        find_entry = ttk.Entry(replace_toplevel, width=30)
        find_entry.grid(row=0, column=1, padx=2, pady=2, sticky="we")
        find_entry.focus_set()

        ttk.Label(replace_toplevel, text="Replace:").grid(row=1, column=0, sticky="e")
        replace_entry = ttk.Entry(replace_toplevel, width=30)
        replace_entry.grid(row=1, column=1, padx=2, pady=2, sticky="we")

        def do_replace():
            find_string = find_entry.get()
            replace_string = replace_entry.get()
            content = self.text_area.get(1.0, tk.END)
            new_content = content.replace(find_string, replace_string)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(1.0, new_content)

        ttk.Button(replace_toplevel, text="Replace All", command=do_replace).grid(row=2, column=1, sticky="e" + "w", padx=2, pady=2)

    def change_font(self):
        font_chooser = tk.Toplevel(self.root)
        font_chooser.title("Choose Font")
        font_chooser.transient(self.root)
        font_chooser.resizable(False, False)

        font_family = tk.StringVar(value=self.current_font[0])
        font_size = tk.IntVar(value=self.current_font[1])

        ttk.Label(font_chooser, text="Font Family:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        family_combo = ttk.Combobox(font_chooser, textvariable=font_family, values=list(font.families()))
        family_combo.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(font_chooser, text="Font Size:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        size_spin = ttk.Spinbox(font_chooser, from_=1, to=100, textvariable=font_size)
        size_spin.grid(row=1, column=1, padx=5, pady=5)

        def apply_font():
            self.current_font = (font_family.get(), font_size.get())
            self.text_area.configure(font=self.current_font)
            font_chooser.destroy()

        ttk.Button(font_chooser, text="Apply", command=apply_font).grid(row=2, column=0, columnspan=2, pady=10)

    def change_color(self):
        colors = colorchooser.askcolor(title="Choose color")
        if colors[1]:
            self.text_area.config(fg=colors[1])

    def toggle_theme(self):
        if self.current_theme == "light":
            self.current_theme = "dark"
        else:
            self.current_theme = "light"
        self.apply_theme()

    def apply_theme(self):
        if self.current_theme == "light":
            self.text_area.config(bg="white", fg="black", insertbackground="black")
            self.root.config(bg="white")
            self.status_bar.config(background="white", foreground="black")
        else:
            self.text_area.config(bg="#2b2b2b", fg="#a9b7c6", insertbackground="white")
            self.root.config(bg="#2b2b2b")
            self.status_bar.config(background="#2b2b2b", foreground="#a9b7c6")

    def show_about(self):
        messagebox.showinfo("About", "Modern Text Editor\nVersion 2.0\nCreated with Python and Tkinter")

if __name__ == "__main__":
    root = tk.Tk()
    editor = ModernTextEditor(root)
    root.mainloop()
