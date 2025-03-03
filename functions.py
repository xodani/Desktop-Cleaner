import shutil
import os 
import glob
from tkinter import *
import tkinter.simpledialog as simpledialog
import subprocess
from tkinter import messagebox 
import send2trash

def users_storage():
    total, used, free = shutil.disk_usage("/")
    total_gb = total/(1000 ** 3)
    total_used = used/(1000 ** 3)
    total_free = free/(1000 ** 3)

    return total_gb, total_used, total_free
            
def display_files(): 
    fileList = []
    dirt = os.path.join(os.path.expanduser("~"), "Desktop")
    
    for item in os.listdir(dirt):
        path = os.path.join(dirt, item)
        if os.path.isdir(path):
            fileList.append(item)
        elif os.path.isfile(path):
            fileList.append(item)
    return fileList

def find(name, listbox, entry):
    filename = name.get()
    dirt = os.path.join(os.path.expanduser("~"), "Desktop")
    
    is_found = False
    
    listbox.delete(0,END)
    for item in os.listdir(dirt):
        if filename in item.lower():
            path = os.path.join(dirt, item)
            if os.path.isdir(path):
                is_found = True
                listbox.insert(END, item)
            elif os.path.isfile(path):
                is_found = True
                listbox.insert(END, item)
    if is_found == False:
        listbox.insert(END, "No file found!")
           
def fill_entry(event,entry,file_list):
    entry.delete(0, END)
    entry.insert(0, file_list.get(ACTIVE))

def selected_file(event, listbox, menu):
    global filename
    item = listbox.curselection()
    if item:
        filename = listbox.get(item[0]) 
        popup_menu(event, menu, listbox)
        print(f"{filename} selected")
    
def open_item():
    dirt = os.path.join(os.path.expanduser("~"), "Desktop")
    path = os.path.join(dirt, filename)
    if os.path.isfile(path):
        subprocess.Popen(['open',path])
    elif os.path.isdir(path):
        subprocess.Popen(['open',path])
    
def rename():
    dirt = os.path.join(os.path.expanduser("~"), "Desktop")
    name = simpledialog.askstring(title="rename", prompt=f"enter new name for {filename}: ")
    if name:
        confirm = messagebox.askyesno("rename", f"are you sure you want to rename {filename}")
        if confirm:
            try:
                old_path = os.path.join(dirt, filename)
                new_path = os.path.join(dirt, name)
                os.rename(old_path, new_path)
                messagebox.showinfo("rename", f"{filename} is now {name}")
            except FileNotFoundError:
                messagebox.showerror("Error", f"File {filename} not found.")
            except Exception as e:
                 messagebox.showerror("Error", f"An error occurred: {e}") 
        else:
            messagebox.showinfo("rename", f"{filename} was not renamed")
                 
def delete():
    dirt = os.path.join(os.path.expanduser("~"), "Desktop")
    confirm = messagebox.askyesno("delete", f"are you sure you want to remove {filename}")
    if confirm:
        path = os.path.join(dirt, filename)
        if os.path.isfile(path):
            delete = messagebox.askyesno("delete", f"are you sure you want to delete {filename}")
            send2trash.send2trash(path)
        elif os.path.isdir(path):
            delete = messagebox.askyesno("delete", f"are you sure you want to delete {filename}")
            send2trash.send2trash(path)
        removed = messagebox.showinfo("delete", f"{filename} had been deleted from your desktop")
            
def back():
    pass

def popup_menu(event, menu, frame):
    menu.post(event.x_root, event.y_root)

def add_folder():
    global folders
    folders = []
    dirt = os.path.join(os.path.expanduser("~"), "Desktop")
    for fold in os.listdir(dirt):
        path = os.path.join(dirt, fold)
        if os.path.isdir(path):
            folders.append(fold)
    return folders

def desk_items():
    
    items = []
    dirt = os.path.join(os.path.expanduser("~"), "Desktop")
    
    for item in os.listdir(dirt):
        path = os.path.join(dirt,item)
        if os.path.isfile(path) and not item.lower().endswith(".zip"):
            items.append(item)
        elif os.path.isdir(path):
            if not os.listdir(path):
                items.append(item)
    return items

            

    
        
        
    

        
    
    

        
        
    
    
    

    
    

    
        
        
    

    
    
        

        
        
    
    
        
   
    
    
    
   
