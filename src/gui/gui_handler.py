import tkinter as tk
from tkinter import filedialog

class GUIHandler:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("XML Editor")

    def run(self):
        tk.Label(self.root, text="XML Editor").pack()
        tk.Button(self.root, text="Select File", command=self.select_file).pack()
        self.root.mainloop()

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
        print(f"Selected file: {file_path}")
