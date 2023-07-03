import os
import sys
import tkinter
from tkinter import *
from tkinter import messagebox, ttk, filedialog
import pandas as pd
#import PythonApplication as pa

def start():
    pass

def stop():
    pass

def save_search():
    pass

def generate_coverletter():
    pass

def display_data(root, df):
    subroot = Toplevel(root)
    subroot.title("!IndeedSearch")
    menubar = Menu(subroot)
    subroot.configure(bg='teal', menu=menubar)
    subroot.option_add('*tearOff', FALSE)

    search_menu = Menu(menubar)
    menubar.add_cascade(label="Search", menu=search_menu)
    #search_menu.add_command(label="Load", command=pa.load_search)
    #search_menu.entryconfigure("Load", accelerator="Ctrl+L")
    search_menu.add_command(label="New", command=lambda: os.startfile(os.path.abspath(__file__)))
    search_menu.entryconfigure("New", accelerator="Ctrl+N")
    #search_menu.add_command(label="Recent", command=pa.recent_search)
    #search_menu.entryconfigure("Recent", accelerator="Ctrl+R")
    search_menu.add_command(label="Save", command=save_search)
    search_menu.entryconfigure("Save", accelerator="Ctrl+S")
    search_menu.add_command(label="Quit", command=lambda: sys.exit())
    search_menu.entryconfigure("Quit", accelerator="Ctrl+Q")

    edit_menu = Menu(menubar)
    menubar.add_cascade(label="Edit", menu=edit_menu)
    edit_menu.add_command(label="Undo", command=lambda: subroot.focus_get().event_generate("<<Undo>>"))
    edit_menu.entryconfigure("Undo", accelerator="Ctrl+U")
    edit_menu.add_command(label="Redo", command=lambda: subroot.focus_get().event_generate("<<Redo>>"))
    edit_menu.entryconfigure("Redo", accelerator="Ctrl+Y")
    edit_menu.add_command(label="Copy", command=lambda: subroot.focus_get().event_generate("<<Copy>>"))
    edit_menu.entryconfigure("Copy", accelerator="Ctrl+C")
    edit_menu.add_command(label="Paste", command=lambda: subroot.focus_get().event_generate("<<Paste>>"))
    edit_menu.entryconfigure("Paste", accelerator="Ctrl+V")
    edit_menu.add_command(label="Select All", command=lambda: subroot.focus_get().event_generate("<<SelectAll>>"))
    edit_menu.entryconfigure("Select All", accelerator="Ctrl+A")

    program_menu = Menu(menubar)
    menubar.add_cascade(label="Program", menu=program_menu)
    program_menu.add_command(label="Restart", command=lambda: os.execl(sys.executable, os.path.abspath(__file__), *sys.argv))
    program_menu.entryconfigure("Restart", accelerator="Ctrl+F5")
    program_menu.add_command(label="Stop", command=stop)
    program_menu.entryconfigure("Stop", accelerator="Ctrl+F6", state=DISABLED)

    options_menu = Menu(menubar)
    menubar.add_cascade(label="Options", menu=options_menu)
    #options_menu.add_command(label="Customize", command=increment_pages_num)
    #options_menu.add_command(label="Keys", command=update_keys)

    help_menu = Menu(menubar)
    menubar.add_cascade(label="Help", menu=help_menu)
    #help_menu.add_command(label="About NotIndeedSearch", command=increment_pages_num)
    help_menu.add_separator()
    #help_menu.add_command(label="README.txt", command=increment_pages_num)

    notebook_data = ttk.Notebook(subroot)
    frame_list = []

    for i in range(len(df)):
        frames = Frame(notebook_data)
        frame_list.append(frames)
        frame_list[i].configure(bd=5, relief='ridge', padx=10, pady=10)
        employer_name = df.loc[i, 'employer_name']
        job_title = df.loc[i, 'job_title']
        page_title = employer_name + ' ^/\^ ' + job_title
        page_label = Label(frame_list[i], text=page_title)
        page_label.pack(side=TOP, padx=5, pady=5)
        text = Text(frame_list[i])
        frame_scrollbar = ttk.Scrollbar(frame_list[i], orient=VERTICAL, command=text.yview)
        text.configure(yscrollcommand=frame_scrollbar.set)
        job_description = df.loc[i, 'job_description']
        text.insert('end', job_description)
        text.pack(side=LEFT, padx=5, pady=5)
        frame_scrollbar.pack(side=RIGHT, fill=Y)
        notebook_data.add(frame_list[i], text=str(i))

    subroot.columnconfigure(0, weight=1, minsize=750)
    notebook_data.grid(row=0, column=0, padx=5, pady=5)
