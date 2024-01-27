import tkinter as tk


root = tk.Tk()
root.geometry("400x400+400+400")
root.title("Test 2")
root.config(bg="lightblue")

label = tk.Label(root, text = "TESTING")
label.pack()



root.mainloop()