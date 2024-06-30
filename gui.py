import tkinter as tk
from tkinter import (filedialog, messagebox, simpledialog)
import subprocess
import customtkinter as ctk
from CTkMenuBar import CTkTitleMenu, CustomDropdownMenu
from pathlib import Path 
import logging
import datetime
import os

root = ctk.CTk()
root.title("Joe's Python Editor")
root.geometry("1150x540")
root.iconbitmap("python_icon.ico")
ctk.set_appearance_mode("Dark")

# Info

current_version = "1.0"
name_program = "Joe-Editor"

# Directory
appdata_dir = Path.home() / "AppData" / "Roaming"
directory = appdata_dir / name_program
directory.mkdir(parents=True, exist_ok=True)

# Logger
def log_settings():
    log_dir = os.path.join(directory, "Logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_filename = os.path.join(log_dir, f"{name_program}_{current_datetime}.log")

    logger = logging.getLogger(f"{name_program}")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger

logger = log_settings()

# Functions
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])
    if file_path:
        with open(file_path, "r") as file:
            code = file.read()
            code_text.delete("1.0", "end")
            code_text.insert("1.0", code)

def save_file():
    code = code_text.get("1.0", "end-1c")
    file_path = filedialog.asksaveasfilename(defaultextension=".py")
    if file_path:
        with open(file_path, "w") as file:
            file.write(code)

def cut_text():
    code_text.event_generate("<<Cut>>")

def copy_text():
    code_text.event_generate("<<Copy>>")

def paste_text():
    code_text.event_generate("<<Paste>>")

def find_text():
    target = simpledialog.askstring("Find", "Enter text to find:")
    if target:
        start_index = code_text.search(target, "1.0", stopindex="end", nocase=True)
        if start_index:
            end_index = f"{start_index}+{len(target)}c"
            code_text.tag_remove("search", "1.0", "end")
            code_text.tag_add("search", start_index, end_index)
            code_text.tag_config("search", background="red")
            code_text.mark_set("insert", start_index)
            code_text.see("insert")

def replace_text():
    target = simpledialog.askstring("Find and Replace", "Enter text to find:")
    if target:
        replace_with = simpledialog.askstring("Find and Replace", "Replace with:")
        if replace_with:
            start_index = code_text.search(target, "1.0", stopindex="end", nocase=True)
            while start_index:
                end_index = f"{start_index}+{len(target)}c"
                code_text.delete(start_index, end_index)
                code_text.insert(start_index, replace_with)
                start_index = code_text.search(target, start_index, stopindex="end", nocase=True)

def clear_text():
    code_text.delete("1.0", "end")

def about():
    about_text = f"Made by jdoherty78. Current version : {current_version}"
    messagebox.showinfo("About", about_text)

def help():
    help_text = "This is a Help section"
    messagebox.showinfo("Help", help_text)

def run_code():
    code = code_text.get("1.0", "end-1c")
    with open(".temp_file.py", "w") as file:
        file.write(code)
    result = subprocess.run(["python", ".temp_file.py"], capture_output=True)
    terminal_text.configure(state=tk.NORMAL)
    terminal_text.insert("end", result.stdout.decode())
    terminal_text.insert("end", result.stderr.decode())
    terminal_text.configure(state=tk.DISABLED)

def clear_code():
    terminal_text.configure(state=tk.NORMAL)
    terminal_text.delete("1.0", "end")
    terminal_text.configure(state=tk.DISABLED)

# Nav
menu = CTkTitleMenu(root)

# File menu
file_menu_btn = menu.add_cascade("File")
file_menu = CustomDropdownMenu(widget=file_menu_btn)
file_menu.add_option(option="Open", command=open_file)
file_menu.add_option(option="Save", command=save_file)
file_menu.add_separator()
file_menu.add_option(option="Exit", command=root.quit)

# Edit menu
edit_menu_btn = menu.add_cascade("Edit")
edit_menu = CustomDropdownMenu(widget=edit_menu_btn)
edit_menu.add_option(option="Cut", command=cut_text)
edit_menu.add_option(option="Copy", command=copy_text)
edit_menu.add_option(option="Paste", command=paste_text)
edit_menu.add_option(option="Find", command=find_text)
edit_menu.add_option(option="Replace", command=replace_text)
edit_menu.add_option(option="Clear", command=clear_text)

# Run menu
run_menu_btn = menu.add_cascade("Run")
run_menu = CustomDropdownMenu(widget=run_menu_btn)
run_menu.add_option(option="Run", command=run_code)
run_menu.add_option(option="Clear", command=clear_code)

# Design menu
design_menu_btn = menu.add_cascade("Design")
design_menu = CustomDropdownMenu(widget=design_menu_btn)
design_menu.add_option(option="Dark", command=lambda: ctk.set_appearance_mode("Dark"))
design_menu.add_option(option="Light", command=lambda: ctk.set_appearance_mode("Light"))

# Help menu
help_menu_btn = menu.add_cascade("Help")
help_menu = CustomDropdownMenu(widget=help_menu_btn)
help_menu.add_option(option="Help", command=help)

# About menu
about_menu_btn = menu.add_cascade("About")
about_menu = CustomDropdownMenu(widget=about_menu_btn)
about_menu.add_option(option="About", command=about)

# Text area - code
text_frame = ctk.CTkFrame(root)
text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

code_text = ctk.CTkTextbox(text_frame, undo=True, maxundo=-1)
code_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

#Text are - output
terminal_frame = ctk.CTkFrame(root)
terminal_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

terminal_text = ctk.CTkTextbox(terminal_frame, state=tk.DISABLED)
terminal_text.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

root.config(menu=menu)
root.mainloop()
