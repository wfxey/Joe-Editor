import tkinter as tk
from tkinter import (filedialog, messagebox, simpledialog)
import subprocess

root = tk.Tk()
root.title("Python Editor v1.0")
root.geometry("400x500+110+340")                   # location of app on screen
root.iconbitmap("python_icon.ico")

# FUNCTIONS

def open_file():
    pass

def save_file():
    pass


# EDIT BUTTONS

def cut_text():
    pass
             

def copy_text():
    pass


def paste_text():
    pass

def clear_text():
    pass

def about():
    about_text = "This is About section"
    messagebox.showinfo("About", about_text)

def help():
    about_text = "This is a Help section"
    messagebox.showinfo("Help", help_text)
    

# RUN CODE FUNCTIONS


# NAVBAR

navbar = tk.Frame(root)
navbar.pack(fill = tk.X)

# DROPDOWN MENU

menu = tk.Menu(navbar)

# BUTTONS


# FILES
file_menu = tk.Menu(menu, tearoff = False)
file_menu.add_command(label="Open", command = open_file)
file_menu.add_command(label="Save", command = save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command = root.quit)
menu.add_cascade(label="File", menu = file_menu)

# EDIT


# ABOUT


# HELP


# RUN

root.config(menu = menu)
# TEXT AREA CODE


# CODE SCROLL BAR


# TEXT AREA TERMINAL


# TERMINAL SCROLL BAR

root.mainloop()
