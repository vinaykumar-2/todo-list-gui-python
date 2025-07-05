# TO-DO-LIST
import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime


#file to store tasks
File_name = "tasks.json"
tasks=[]

#load tasks from json
def load_tasks():
    global tasks
    try:
        with open(File_name,"r") as f:
            tasks=json.load(f)
    except FileNotFoundError:
        tasks=[]
    
#save curent tasks    
def save_tasks():
    with open(File_name,"w") as f:
        json.dump(tasks,f,indent=4)

#add a new task
def add_task():
    name = entry_task.get().strip()
    due_date = entry_due.get().strip()
    priority = combo_priority.get()

    #check if fields are empty
    if not name or not due_date:
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return
    
    #validate date format
    try:
        datetime.strptime(due_date,"%Y-%m-%d")
    except ValueError:
        messagebox.showwarning("Date Format", "use YYYY-MM-DD format.")
        return

    #create task dictionary
    task ={
        "name": name,
        "due_date": due_date,
        "priority": priority,
        "done": False
    }

    #add to task list and update
    tasks.append(task)
    save_tasks()
    refresh_tasks()
    clear_inputs()

#clear all fields
def clear_inputs():
    entry_task.delete(0,tk.END)
    entry_due.delete(0,tk.END)
    combo_priority.set("Medium")

#refresh the table to show latest tasks
def refresh_tasks():
    #remove all current rows
    tree.delete(*tree.get_children())

    #insert updated tasks
    for i, task in enumerate(tasks):
        status ="Done" if task["done"] else "Pending"
        tree.insert("","end" , iid=i,values=(task['name'],task['due_date'],task['priority'],status))

#mark selected task as done
def mark_done():
    selected = tree.selection()
    if selected:
        index = int(selected[0])
        tasks[index]['done'] =True
        save_tasks()
        refresh_tasks()

#delete selected tasks from list
def delete_task():
    selected = tree.selection()
    if selected:
        index = int(selected[0])
        del tasks[index]
        save_tasks()
        refresh_tasks()

#GUI

#create main window
root = tk.Tk()
root.title("To-Do List")
root.geometry("600x400")

#frame for inputs
frame = tk.Frame(root)
frame.pack(pady=10)

#task name input
tk.Label(frame,text="Task Name: ").grid(row=0,column=0)
entry_task = tk.Entry(frame,width=25)
entry_task.grid(row=0,column=1,padx=5)

#due date input
tk.Label(frame,text="Due Date (YYYY-MM-DD): ").grid(row=1,column=0)
entry_due = tk.Entry(frame,width=25)
entry_due.grid(row=1,column=1,padx=5)

#priority dropdown
tk.Label(frame,text="Priority:").grid(row=2,column=0)
combo_priority = ttk.Combobox(frame,values=["High","Medium","Low"],width=22)
combo_priority.set("Medium")
combo_priority.grid(row=2,column=1,padx=5)

#add task button
btn_add = tk.Button(root,text="Add Task",command=add_task)
btn_add.pack(pady=5)

#tree view to show tasks
columns = ("Task", "Due Date", "Priority", "Status")
tree = ttk.Treeview(root ,columns=columns,show="headings")
for col in columns:
    tree.heading(col,text=col)  #column titles
tree.pack(fill=tk.BOTH,expand=True,pady=10)

#buttons to perform tasks
btn_frame = tk.Frame(root)
btn_frame.pack(pady=5)

tk.Button(btn_frame,text="Mark Done",command=mark_done).grid(row=0,column=0,padx=10)
tk.Button(btn_frame,text="Delete Task",command=delete_task).grid(row=0, column=1, padx=10)

#load saved tasks and show them
load_tasks()
refresh_tasks()

#start GUI loop
root.mainloop()