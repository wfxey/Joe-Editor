import tkinter as tk
from tkinter import (filedialog, messagebox, simpledialog)
import subprocess

root = tk.Tk()
root.title("Joe's Python Editor v1.9123416546584651")
root.geometry("+250+340")                   # location of app on screen
root.iconbitmap("python_icon.ico")

# FUNCTIONS

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Python Files", "*.py")])  #("Python Files", "*.py"), ("JavaScript", "*.js")  -- also javascript files

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


# EDIT BUTTONS

def cut_text():
    code_text.event_generate("<<Cut>>")
             

def copy_text():
    code_text.event_generate("<<Copy>>")


def paste_text():
    code_text.event_generate("<<Paste>>")

def find_text():
    target = simpledialog.askstring("Find", "Enter text to find: ")
    #print(target)
    if target:
        start_index = code_text.search(target, "1.0", stopindex="end", nocase = True)
        # HELLO, hello, Hello
        if start_index:
            end_index = f"{start_index}+{len(target)}c"
            code_text.tag_remove("search", "1.0", "end")
            code_text.tag_add("search", start_index, end_index)
            code_text.tag_config("search", background="red")
            code_text.mark_set("insert", start_index)
            code_text.see("insert")

def replace_text():
    target = simpledialog.askstring("Find and Replace", "Enter text to find: ")
    #print(target)
    if target:
        replace_with = simpledialog.askstring("Find and Replace", "Replace with:")
        #print(replace_with)
        if replace_with:
            start_index = code_text.search(target, "1.0", stopindex = "end", nocase = True)

            while start_index:
                end_index = f"{start_index}+{len(target)}c"
                code_text.delete(start_index, end_index)
                code_text.insert(start_index, replace_with)
                start_index = code_text.search(target, start_index, stopindex = "end", nocase = True)

def clear_text():
    code_text.delete("1.0", "end")   # left side text box

def about():
    about_text = "This is About section"
    messagebox.showinfo("About", about_text)

def help():
    help_text = "This is a Help section"
    messagebox.showinfo("Help", help_text)
    

# RUN CODE FUNCTIONS
def run_code():
    code = code_text.get("1.0", "end-1c")
    with open(".temp_file.py", "w") as file:      # create hidden temp file to store code
        file.write(code)
    result = subprocess.run(["python", ".temp_file.py"], capture_output = True)
    terminal_text.insert("end", result.stdout.decode())
    terminal_text.insert("end", result.stderr.decode())

def clear_code():
    terminal_text.delete("1.0", "end")    # right side text box, terminal area
    
# NAVBAR

navbar = tk.Frame(root)
navbar.pack(fill = tk.X)

# DROPDOWN MENU

menu = tk.Menu(navbar)

# BUTTONS BELOW


# FILES Menu
file_menu = tk.Menu(menu, tearoff = False)
file_menu.add_command(label="Open", command = open_file)
file_menu.add_command(label="Save", command = save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command = root.quit)
menu.add_cascade(label="File", menu = file_menu)

# EDIT Menu

edit_menu = tk.Menu(menu, tearoff=False)
edit_menu.add_command(label="Cut", command = cut_text)
edit_menu.add_command(label="Copy", command = copy_text)
edit_menu.add_command(label="Paste", command = paste_text)
edit_menu.add_command(label="FIND", command = find_text)
edit_menu.add_command(label="REPLACE", command = replace_text)
edit_menu.add_command(label="Clear", command = clear_text)

menu.add_cascade(label="Edit", menu = edit_menu)

# ABOUT Menu

about_menu = tk.Menu(menu, tearoff=False)
about_menu.add_command(label="About", command = about)
menu.add_cascade(label="About", menu = about_menu)

# HELP Menu

help_menu = tk.Menu(menu, tearoff=False)
help_menu.add_command(label="Help", command = help)
menu.add_cascade(label="Help", menu = help_menu)

#1 RUN

run_menu = tk.Menu(menu, tearoff = False)
run_menu.add_command(label="Run", command = run_code)
run_menu.add_command(label="Clear", command = clear_code)
menu.add_cascade(label="Run", menu = run_menu)

# TEXT AREA CODE

text_frame = tk.Frame(root)
text_frame.pack(side = tk.LEFT, fill=tk.BOTH, expand = True)

code_text = tk.Text(text_frame, undo = True, maxundo = -1)
code_text.pack(side = tk.LEFT, fill=tk.BOTH, expand = True)

# CODE SCROLL BAR

text_scroll = tk.Scrollbar(text_frame, command = code_text.yview, orient = tk.VERTICAL)
text_scroll.pack(side = tk.RIGHT, fill=tk.Y)
code_text.config(yscrollcommand = text_scroll.set)

# TEXT AREA TERMINAL
terminal_frame = tk.Frame(root)
terminal_frame.pack(side = tk.RIGHT, fill=tk.BOTH, expand = True)

terminal_text = tk.Text(terminal_frame, bg="black", fg="white", insertbackground="white")
terminal_text.pack(side = tk.RIGHT, fill=tk.BOTH, expand = True)

# TERMINAL SCROLL BAR

terminal_scroll = tk.Scrollbar(terminal_frame, command = terminal_text.yview, orient = tk.VERTICAL)
terminal_scroll.pack(side = tk.RIGHT, fill=tk.Y)
terminal_text.config(yscrollcommand = terminal_scroll.set)

# TERMINAL SCROLL BAR

root.config(menu = menu)
root.mainloop()
