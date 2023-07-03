import os
import sys
import threading
import time
import tkinter
from tkinter import *
from tkinter import messagebox, ttk, filedialog
import pandas as pd
import requests
import ReadJSearchData as js

def start():
    global interrupt, progressbar_thread, submit_thread
    interrupt = False
    submit_button.configure(text='Stop', command=stop)
    program_menu.entryconfigure("Stop", state=NORMAL)
    search_menu.entryconfigure("Submit", state=DISABLED)
    progressbar_thread = threading.Thread(target=update_progressbar, args=(submit_progressbar,))
    submit_thread = threading.Thread(target=on_submit)
    progressbar_thread.start()
    submit_thread.start()

def check_threads():
    if not progressbar_thread.is_alive() and not submit_thread.is_alive():
        progressbar_thread.join()
        submit_thread.join()

def stop():
    global interrupt
    interrupt = True
    submit_button.configure(text='Submit', command=start)
    search_menu.entryconfigure("Submit", state=NORMAL)
    program_menu.entryconfigure("Stop", state=DISABLED)
    root.after(1000, check_threads)

def update_progressbar(submit_progressbar):
    i = 0
    while not interrupt:
        time.sleep(0.004)
        submit_progressbar['value'] = i
        i += 1
    submit_progressbar['value'] = 0

def on_submit():
    try:
        with open(os.environ.get('Beans'), 'r') as file:
            API_key = file.read()
    except Exception as e:
        answer = messagebox.askyesno(message='No Valid Keys Found. Update Keys?', icon='question', title='Error')
        if answer:
            update_keys()
            root.after(1000, stop)
            return
        else:
            root.after(1000, stop)
            return
    
    url = "https://jsearch.p.rapidapi.com/search"
    querystring = {
        "query": query.get(),
        "page": "1",
        "num_pages": pages_num.get(),
        "date_posted": date_posted.get(),
        "remote_jobs_only": remote_jobs_only.get(),
        "employment_types": employment_type.get(),
        "job_requirements": job_requirement.get()
    }
    headers = {
        "X-RapidAPI-Key": API_key,
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    try:
        response = requests.get(url, headers=headers, params=querystring)
        data = response.json()
        value = data['data']
    except Exception as e:
        root.after(2000, stop)
        messagebox.showinfo("on_submit error", "Job search data not found.")
        return

    df = pd.DataFrame(value)
    fd = pd.DataFrame(columns=querystring.keys())
    fd.loc[0] = querystring.values()
    df = df.join(fd)
    try:
        df.to_excel(save_file)
    except Exception as e:
        df.to_excel('jsearch_data.xlsx')
    root.after(3000, stop)
    js.display_data(root, df)

def query_help_prompt():
    messagebox.showinfo("Help", "Free-form jobs search query. It is highly recommended to include job title and location as part of the query.")

def increment_pages_num():
    global page_counter
    if page_counter < 20:
        page_counter += 1
        pages_num.set(str(page_counter))
        pages_num_label.configure(text=str(page_counter))

def decrement_pages_num():
    global page_counter
    if page_counter > 1:
        page_counter -= 1
        pages_num.set(str(page_counter))
        pages_num_label.configure(text=str(page_counter))

def load_search():
    load_file = filedialog.askopenfilename()
    df = pd.read_excel(load_file, engine='openpyxl')
    js.display_data(root, df)

def save_search():
    global save_file
    save_file = filedialog.asksaveasfilename()
    querystring = {"query":query.get(),"page":"1","num_pages":pages_num.get(),"date_posted":date_posted.get(),"remote_jobs_only":remote_jobs_only.get(),"employment_types":employment_type.get(),"job_requirements":job_requirement.get()}
    df = pd.DataFrame(columns=querystring.keys())
    df.loc[0] = querystring.values()
    df.to_excel(save_file)

def recent_search():
    files = os.listdir(os.path.dirname(__file__))
    files = [os.path.join(os.path.dirname(__file__), file) for file in files]
    files = [file for file in files if os.path.isfile(file)]
    files.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    recent_file = files[0]
    df = pd.read_excel(recent_file, engine='openpyxl')
    js.display_data(root, df)

def update_keys():
    global Nigga
    Nigga = filedialog.askopenfilename()
    
global root
root = Tk()
root.title("!IndeedSearch")
menubar = Menu(root)
root.configure(bg='teal', menu=menubar)
root.option_add('*tearOff', FALSE)

search_menu = Menu(menubar)
menubar.add_cascade(label="Search", menu=search_menu)
search_menu.add_command(label="Submit", command=start)
search_menu.entryconfigure("Submit", accelerator="Ctrl+ENTER")
search_menu.add_command(label="Load", command=load_search)
search_menu.entryconfigure("Load", accelerator="Ctrl+L")
search_menu.add_command(label="New", command=lambda: os.startfile(os.path.abspath(__file__)))
search_menu.entryconfigure("New", accelerator="Ctrl+N")
search_menu.add_command(label="Recent", command=recent_search)
search_menu.entryconfigure("Recent", accelerator="Ctrl+R")
search_menu.add_command(label="Save", command=save_search)
search_menu.entryconfigure("Save", accelerator="Ctrl+S")
search_menu.add_command(label="Quit", command=lambda: sys.exit())
search_menu.entryconfigure("Quit", accelerator="Ctrl+Q")

edit_menu = Menu(menubar)
menubar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Undo", command=lambda: root.focus_get().event_generate("<<Undo>>"))
edit_menu.entryconfigure("Undo", accelerator="Ctrl+U")
edit_menu.add_command(label="Redo", command=lambda: root.focus_get().event_generate("<<Redo>>"))
edit_menu.entryconfigure("Redo", accelerator="Ctrl+Y")
edit_menu.add_command(label="Copy", command=lambda: root.focus_get().event_generate("<<Copy>>"))
edit_menu.entryconfigure("Copy", accelerator="Ctrl+C")
edit_menu.add_command(label="Paste", command=lambda: root.focus_get().event_generate("<<Paste>>"))
edit_menu.entryconfigure("Paste", accelerator="Ctrl+V")
edit_menu.add_command(label="Select All", command=lambda: root.focus_get().event_generate("<<SelectAll>>"))
edit_menu.entryconfigure("Select All", accelerator="Ctrl+A")

program_menu = Menu(menubar)
menubar.add_cascade(label="Program", menu=program_menu)
program_menu.add_command(label="Restart", command=lambda: os.execl(sys.executable, os.path.abspath(__file__), *sys.argv))
program_menu.entryconfigure("Restart", accelerator="Ctrl+F5")
program_menu.add_command(label="Stop", command=stop)
program_menu.entryconfigure("Stop", accelerator="Ctrl+F6", state=DISABLED)

options_menu = Menu(menubar)
menubar.add_cascade(label="Options", menu=options_menu)
options_menu.add_command(label="Customize", command=increment_pages_num)
options_menu.add_command(label="Keys", command=update_keys)

help_menu = Menu(menubar)
menubar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="About NotIndeedSearch", command=increment_pages_num)
help_menu.add_separator()
help_menu.add_command(label="README.txt", command=increment_pages_num)

num_frames = 6
frame_list = []

for i in range(num_frames):
    frames = Frame(root)
    frame_list.append(frames)

for row in range(2):
    for col in range(3):
        root.columnconfigure(col, weight=1, minsize=300)
        if row * 3 + col == 0 or row * 3 + col == 3:
            frame_list[row * 3 + col].grid(row=row, column=col)
        frame_list[row * 3 + col].grid(row=row + col, column=col)
        frame_list[row * 3 + col].configure(bd=5, relief='ridge', padx=10, pady=10)

query_label = Label(frame_list[0], text="Query: ")
query_label.pack(side=LEFT, padx=5, pady=5)
query = Entry(frame_list[0])
query.pack(side=LEFT, padx=5, pady=5)
query_help = Button(frame_list[0], text="?", command=query_help_prompt)
query_help.pack(side=LEFT, padx=5, pady=5)

pages_label = Label(frame_list[1], text="Page(s): ")
pages_label.pack(side=LEFT, padx=5, pady=5)
page_counter = 1
pages_num = StringVar(root)
pages_num.set(str(page_counter))
pages_num_label = Label(frame_list[1], text=str(page_counter))
pages_num_label.pack(side=LEFT, padx=5, pady=5)
inc_button = Button(frame_list[1], text="+", command=increment_pages_num)
inc_button.pack(side=LEFT, padx=5, pady=5)
dec_button = Button(frame_list[1], text="-", command=decrement_pages_num)
dec_button.pack(side=LEFT, padx=5, pady=5)

date_posted_label = Label(frame_list[2], text="Date Posted: ")
date_posted_label.pack(side=LEFT, padx=5, pady=5)
date_posted = StringVar(root)
date_posted.set("all")
date_posted_options = ["all","today","3days","week","month"]
dp_drop_down = OptionMenu(frame_list[2],date_posted,*date_posted_options)
dp_drop_down.pack(side=LEFT, padx=5, pady=5)

remote_jobs_label = Label(frame_list[3], text="Remote Jobs Only: ")
remote_jobs_label.pack(side=LEFT, padx=5, pady=5)
remote_jobs_only = StringVar(value="false")
remote_jobs_true = Radiobutton(frame_list[3], text="true", variable=remote_jobs_only, value="true")
remote_jobs_true.pack(side=LEFT, padx=5, pady=5)
remote_jobs_false = Radiobutton(frame_list[3], text="false", variable=remote_jobs_only, value="false")
remote_jobs_false.pack(side=LEFT, padx=5, pady=5)

employment_type_label = Label(frame_list[4], text="Employment Type: ")
employment_type_label.pack(side=LEFT, padx=5, pady=5)
employment_type = StringVar(root)
employment_type.set("FULLTIME")
employment_type_options = ["FULLTIME","CONTRACTOR","PARTTIME","INTERN"]
et_drop_down = OptionMenu(frame_list[4],employment_type,*employment_type_options)
et_drop_down.pack(side=LEFT, padx=5, pady=5)

job_requirement_label = Label(frame_list[5], text="Job Requirement: ")
job_requirement_label.pack(side=LEFT, padx=5, pady=5)
job_requirement = StringVar(root)
job_requirement.set("under_3_years_experience")
job_requirement_options = ["under_3_years_experience","more_than_3_years_experience","no_experience","no_degree"]
jr_drop_down = OptionMenu(frame_list[5],job_requirement,*job_requirement_options)
jr_drop_down.pack(side=LEFT, padx=5, pady=5)

submit_button = Button(root, text="Submit", command=start)
submit_button.grid(row=4, column=2, padx=10, pady=10)

submit_progressbar = ttk.Progressbar(root, mode='determinate', maximum=100)
submit_progressbar.grid(row=5, column=2, padx=10, pady=10)

try:
    root.mainloop()
except SystemExit:
    root.destroy()
