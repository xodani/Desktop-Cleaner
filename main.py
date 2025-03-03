from tkinter import *
from PIL import Image, ImageTk
import functions
import os
import tkinter.simpledialog as simpledialog
import shutil
from tkinter import messagebox 
import send2trash
import subprocess

class DesktopCleaner:
    
    def __init__(self, window):
        self.window = window
        self.window.minsize(415 , 415)
        self.window.maxsize(415 , 415)
        self.window.title("Desktop Cleaner")
        self.window.resizable(False, False)
        
        self.main_frame = Frame(window, bg="#826786")
        self.organize_frame = Frame(window, bg="#301814")
        self.trash_or_keep_frame = Frame(window, bg="#8d5159")
        self.folders_frame = Frame(window, bg="#8d5159")
        
        self.goto_main()

    def clear(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()
        
    def goto_main(self):
        self.clear(self.main_frame)
        self.main_frame.pack(fill=BOTH, expand=True)
        
        self.organize_frame.pack_forget()
        self.trash_or_keep_frame.pack_forget()     
        
        self.main_setup()
    
    def goto_org(self):
        self.clear(self.organize_frame)
        self.organize_frame.pack(fill=BOTH, expand=True)
        
        self.main_frame.pack_forget()
        self.trash_or_keep_frame.pack_forget()
        self.folders_frame.pack_forget()
        
        self.organize_setup()
           
    def goto_tok(self):
        self.clear(self.trash_or_keep_frame)
        self.trash_or_keep_frame.pack(fill=BOTH, expand=True)
        
        self.main_frame.pack_forget()
        self.organize_frame.pack_forget()
        
        self.tok_setup()
    
    def add_image(self,frame,image):
        pic = Image.open(image)
        pic = pic.resize((415,415), Image.Resampling.LANCZOS)
        photo_image = ImageTk.PhotoImage(pic)
        image_label = Label(frame, image=photo_image)
        image_label.pack()
        
        image_label.image = photo_image
    
    def main_setup(self):
        total_gb, total_used, total_free = functions.users_storage()
        Label(self.main_frame, text="Desktop cleaner", bg="#826786").pack(side=TOP, pady=10, anchor="n")
        
        storage= StringVar()
        used= StringVar()
        free= StringVar()
        
        storage.set(f"Total PC Space: {total_gb:.2f}")
        used.set(f"Space Used: {total_used:.2f}")
        free.set(f"Total Free: {total_free:.2f}")
        
        labelsFrame = Frame(self.main_frame, bg="#826786")
        labelsFrame.pack(side=TOP, pady=8, fill= X)
        Label(labelsFrame, textvariable=used, font=("Arial", 10)).pack(side=LEFT, padx=5)
        Label(labelsFrame, textvariable=storage, font=("Arial", 10)).pack(side=LEFT, padx=5)
        Label(labelsFrame, textvariable=free, font=("Arial", 10)).pack(side=RIGHT, padx=5)
        
        buttonsFrame = Frame(self.main_frame, bg="#826786")
        buttonsFrame.pack(side=BOTTOM, pady=8,fill=X)
        Button(buttonsFrame, text="Organize", command=self.goto_org).pack(side=LEFT,padx=5)
        Button(buttonsFrame, text="Trash or Keep", command=self.goto_tok).pack(side=RIGHT,padx=5)
        
        self.add_image(self.main_frame,'images/coffee.jpg')
       
    def organize_setup(self):
        Label(self.organize_frame, text="Organize").pack(side=TOP, pady=10, anchor="n")
        Button(self.organize_frame, text="Main", command=self.goto_main).pack(side=BOTTOM, padx=5)
        
        searchFrame = Frame(self.organize_frame)
        searchFrame.pack(fill=X, side=TOP)
        Label(searchFrame, text="Find file or folder").pack(side=LEFT)

        user_file = StringVar()
        Button(searchFrame, text="Search", command=lambda: functions.find(user_file, listbox, entry)).pack(side=RIGHT)
        
        entry = Entry(searchFrame, textvariable = user_file, font=('arial', 10))
        entry.pack(side=LEFT)
        
        listbox = Listbox(self.organize_frame, height=50, width=15,bg="brown", font=('arial', 8))
        listbox.pack(side=LEFT, padx=5, pady=5)
        
        entry.bind("<KeyRelease>", lambda event: functions.find(user_file, listbox, entry))
         
        for files in functions.display_files():
            listbox.insert(END, files)
        listbox.bind("<Double-Button-1>", lambda event: functions.selected_file(event,listbox,menu))
             
        fillout = functions.fill_entry
        listbox.bind("<<ListboxSelect>>",lambda event: fillout(Event, entry, listbox))
        
        scroll = Scrollbar(self.organize_frame)
        scroll.pack(side=LEFT, padx=5, pady=5)
        
        listbox.config(yscrollcommand = scroll.set)
        scroll.config(command = listbox.yview)
        
        def update_listbox():
            listbox.delete(0, END)
            for files in functions.display_files():
                listbox.insert(END, files)
                listbox.bind("<Double-Button-1>", lambda event: functions.selected_file(event,listbox,menu))
                
            
        
        def delete():
            filename = functions.filename
            dirt = os.path.join(os.path.expanduser("~"), "Desktop")
            confirm = messagebox.askyesno("delete", f"are you sure you want to remove {filename}")
            if confirm:
                path = os.path.join(dirt, filename)
                if os.path.isfile(path):
                    delete = messagebox.askyesno("delete", f"are you sure you want to delete {filename}")
                    send2trash.send2trash(path)
                    update_listbox()
                elif os.path.isdir(path):
                    delete = messagebox.askyesno("delete", f"are you sure you want to delete {filename}")
                    send2trash.send2trash(path)
                    update_listbox()
                removed = messagebox.showinfo("delete", f"{filename} had been deleted from your desktop")   
        
        menu = Menu(self.organize_frame, tearoff=False)
        menu.add_command(label="Move" , command=self.goto_move)
        menu.add_command(label="Open", command=functions.open_item)
        menu.add_command(label="Rename", command=functions.rename)
        menu.add_command(label="Delete", command=delete)
        menu.add_separator()
        menu.add_command(label="Back", command=functions.back)
        
        self.organize_frame.bind("<Button-3>", lambda event: functions.popup_menu(event, menu, self.organize_frame))
        self.add_image(self.organize_frame,'images/1.png')   
        
    def tok_setup(self):
        item_list = functions.desk_items()
        self.counter = 0
        
        if item_list:
            item = item_list[self.counter]
        else:
            item = "No files or empty folders found"
        
        img = Image.open("images/cat.jpg")
        resize = img.resize((400,400))
        left = Image.open("images/trash.png")
        right = Image.open("images/keep.png")
        
        leftsize = left.resize((50,50), Image.LANCZOS)
        rightsize = right.resize((50,50), Image.LANCZOS)
        
        self.trashImage = ImageTk.PhotoImage(leftsize)
        self.keepImage = ImageTk.PhotoImage(rightsize)
        
        def view():
            dirt = os.path.join(os.path.expanduser("~"), "Desktop")
            path = os.path.join(dirt, item_list[self.counter])
            if os.path.isfile(path):
                subprocess.Popen(['open',path])
            elif os.path.isdir(path):
                subprocess.Popen(['open',path])
            
  
        Label(self.trash_or_keep_frame, text="Trash or Keep", bg="#8d5159").pack(side=TOP, pady=10, anchor="n")
        Button(self.trash_or_keep_frame, text="Main", command=self.goto_main, bg="#8d5159").pack(side=TOP, pady=10)
        Button(self.trash_or_keep_frame, text="open", command=view).pack(side=BOTTOM)
        
        trash_button = Button(self.trash_or_keep_frame, image = self.trashImage, text="left", borderwidth=0, command=lambda: trash())
        trash_button.pack(side=LEFT)
        keep_button = Button(self.trash_or_keep_frame,image = self.keepImage, text="right", borderwidth=0, command=lambda: keep())
        keep_button.pack(side=RIGHT)
        
        canvas = Canvas(self.trash_or_keep_frame, bg="#8d5159")
        canvas.pack(side=TOP, expand=True, fill=BOTH)
        canvas.image = ImageTk.PhotoImage(resize)
        canvas.create_image(120,120, image = canvas.image)
        
     
        #Label(self.trash_or_keep_frame, text="trash").pack(side=LEFT)
        #Label(self.trash_or_keep_frame, text="keep").pack(side=RIGHT)
        
        back = Button(self.trash_or_keep_frame, text="back", command=lambda:back())
        back.pack(side=LEFT)
        nextitem = Button(self.trash_or_keep_frame, text="next", command=lambda:nextItem())
        nextitem.pack(side=RIGHT)
        
        fileLabel = Label(canvas, text=item,font=("Arial", 12))
        fileLabel.pack(side=BOTTOM)
        
        def nextItem():
            try:
                dirt = os.path.join(os.path.expanduser("~"), "Desktop")
                path = os.path.join(dirt, item_list[self.counter])
            
                self.counter += 1
                
                if self.counter < len(item_list) - 1:
                    fileLabel.config(text=item_list[self.counter])
                else:
                    fileLabel.config(text="No more folders or files")
                    
            except Exception:
                fileLabel.config(text="No more folders or files")
                print("no more items")
                
        def back():
            try:
                dirt = os.path.join(os.path.expanduser("~"), "Desktop")
                path = os.path.join(dirt, item_list[self.counter])
                
                if self.counter > 0:
                    self.counter -= 1
                    fileLabel.config(text=item_list[self.counter])
                else:
                    fileLabel.config(text=item_list[0])
                    
            except Exception:
                fileLabel.config(text="No more folders or files")
                print("no more items")
            
            
            
        def trash():
            try:
                dirt = os.path.join(os.path.expanduser("~"), "Desktop")
                path = os.path.join(dirt, item_list[self.counter])
                send2trash.send2trash(path)
            
                self.counter += 1
                
                if self.counter < len(item_list) - 1:
                    fileLabel.config(text=item_list[self.counter])
                else:
                    fileLabel.config(text="No more folders or files")
                    
            except Exception:
                fileLabel.config(text="No more folders or files")
                print("no more items")
                
                    
        def keep():
            try:
                self.counter += 1
                
                if self.counter < len(item_list) - 1:
                    fileLabel.config(text=item_list[self.counter])
                else:
                    fileLabel.config(text="No more folders or files")
            except Exception:
                fileLabel.config(text="No more folders or files")
                print("no more items")
            
    def goto_move(self):
        self.clear(self.folders_frame)
        self.folders_frame.pack(fill=BOTH, expand=True)
        
        self.main_frame.pack_forget()
        self.organize_frame.pack_forget()
        self.trash_or_keep_frame.pack_forget()
        
        self.folders_setup()
    
    def folders_setup(self):
        filename = functions.filename
        print(f"for {filename}")
        
        labelsFrame = Frame(self.folders_frame)
        labelsFrame.pack(side=TOP)
        Label(self.folders_frame, text="Folders", bg="#826786").pack(side=TOP, anchor="n")
        createButton = Button(self.folders_frame, text="create folder", bg="#826786")
        createButton.pack(side=TOP, pady=5,anchor="n")
        Button(self.folders_frame, text="back", command=self.goto_org).pack(side=BOTTOM, anchor="s")
        
        Label(self.folders_frame, text=f"Working with: {filename}").pack(side=TOP, anchor="s")
        image = Image.open("images/fold.png")
        fold_img = image.resize((70,70))
        
        canvas = Canvas(self.folders_frame)
        
        scrolly = Scrollbar(self.folders_frame, orient=VERTICAL, command=canvas.yview)
        scrolly.pack(side=RIGHT, fill=Y)
        
        scrollx = Scrollbar(self.folders_frame, orient=HORIZONTAL, command=canvas.xview)
        scrollx.pack(side=BOTTOM, fill=X)
        
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        
        canvas.configure(yscrollcommand=scrolly.set, xscrollcommand=scrollx.set)
        
        canvasFrame = Frame(canvas)
        canvas.create_window((0,0), window=canvasFrame, anchor="nw")

        #canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        self.image_refs = []
        row = 0
        col = 0
        functions.add_folder()
        
        def move(name):
            confirm = messagebox.askyesno("Move", f"Are you sure you want to move {filename} to {name}?")
            desk = os.path.join(os.path.expanduser("~"), "Desktop")
            curr_path = os.path.join(desk, filename)
            go_path = os.path.join(desk, name)
            
            print(f"moving {functions.filename} to {name} ")
            if confirm:
                shutil.move(curr_path, go_path)
                messagebox.showinfo("Done", f"{filename} has been moved to {name}")
                self.goto_org()
            else:
                messagebox.showinfo("Unsuccessful", f"{filename} has not been moved")
            
        def add_image(row, col, folder):
            img = ImageTk.PhotoImage(fold_img)
            self.image_refs.append(img)
            
            imageLabel = Label(canvasFrame, image=img)
            imageLabel.grid(row=row, column=col, padx=5)
            
            nameLabel = Label(canvasFrame, text=folder, font=("Arial", 8), wraplength=100)
            nameLabel.grid(row=row , column=col)
            
            imageLabel.bind("<Button-1>", lambda event, name=folder: move(name))
            
        def add_folders():
            row = 0
            col = 0
            for folder in functions.folders:
                #print(f"added {folder} at {row} , {col}")
                add_image(row, col, folder)
                col += 1
                if col == 4:
                    row+= 1
                    col = 0

        def update(frame):
            for widget in frame.winfo_children():
                widget.destroy()
            
            folders = functions.add_folder()
            add_folders()
                    
        def new_folder(frame):
            global cleaner
            cwd = os.getcwd()
            print(f" current: {cwd}")
            desktop = os.path.expanduser("~/Desktop")
            os.chdir(desktop)
            cwd = os.getcwd()
            print(f"new: {cwd}")
    
            name = simpledialog.askstring(title="new folder", prompt="enter folder name: ")
    
            try:
                os.makedirs(name)
                print(f"created {name}")
                update(canvasFrame)
            except FileExistsError:
                print(f"there is folder named: {name}")
            except PermissionError:
                print(f"Permission denied: Unable to create '{name}'.")
            except Exception as e:
                print(f"An error occurred: {e}")        
           
        createButton.bind("<Button-1>", new_folder)
             
        add_folders()
        
        canvasFrame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))

        
window = Tk() 
app = DesktopCleaner(window)
window.mainloop()

