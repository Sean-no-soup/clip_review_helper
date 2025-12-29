import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import os
import dbm

root = tk.Tk()  # Create the main window
root.geometry("700x350")

class Dirbutton(tk.Frame):
    directory = ""

    def __init__(self, parent, label_text="label_text"):
        super().__init__(master = parent)
        self.rowconfigure((0,1), weight = 1, uniform='a')
        self.columnconfigure(0, weight = 1, uniform='a')
        self.label = tk.Label(self, text = label_text, bg="grey")
        self.label.grid(row = 0, column = 0, sticky = 'nsew')
        self.button = tk.Button(self, text= "select directory",bg="grey",\
            command = self.click_function)
        self.button.grid(row=1, column=0, sticky = 'nsew')
        self.pack(expand = True, fill = tk.X, side=tk.LEFT)

    def click_function(self):
        dirpath = tk.filedialog.askdirectory(mustexist=True).replace("/","\\")+"\\"
        if dirpath=="" or dirpath=="\\":return
        self.directory = dirpath

        if len(dirpath) > 32: #long directory check and display format
            self.button.config(text=f"{dirpath[:9]}...{dirpath[-23:]}")

        else:
            self.button.config(text=dirpath)

class Sourcebutton(Dirbutton):
    directory = ""
    fileList = []
    num_files = 0
    index = 0

    def click_function(self): #select directory
        dirpath = tk.filedialog.askdirectory(mustexist=True).replace("/","\\")+"\\"
        if dirpath=="":return
        self.directory = dirpath

        if len(dirpath) > 32: #long directory check and display format
            self.button.config(text=f"{dirpath[:9]}...{dirpath[-23:]}")
        else:
            self.button.config(text=dirpath)

        for file in os.listdir(dirpath):
            if file.endswith(".mp4"):
                self.fileList.append(file)
                self.num_files += 1

        self.update_db()

    def update_db(self, flag="", value=""):
        dbpath = f'{self.directory}\\queued cache'
        with dbm.open(dbpath, 'c') as db:
            delete_key_list = []
            move_key_list = []
            for key in list(db):
                if db[key].decode("utf-8").split("::")[0] == "-1":
                    delete_key_list.append(key.decode("utf-8"))
                    #print(f"delete {key}")
                
                elif db[key].decode("utf-8").split("::")[0] in "1234":
                    print( f"invalid action {db[key]}{key} ")
                    raise AssertionError

                elif db[key].decode("utf-8").split("::")[0] == "0":
                    pass #no action

                else:
                    move_key_list.append(key.decode("utf-8"))
                    #print(f"move {key.decode("utf-8")} to {db[key].decode("utf-8").split("::")[0]}")

            confirm_delete = tk.messagebox.askokcancel(title=f"CONFIRM", message=f"delete {len(delete_key_list)} files?")

            if not confirm_delete:
                return #exit early

            for key in delete_key_list:
                delete_path = f"{self.directory}{key}"

                if os.path.exists(delete_path):
                    try:
                        os.remove(delete_path)
                        del db[key]
                    except:
                        print(f"could not delete {delete_path}")
                        raise Exception
                else:
                    print(f"{delete_path} does not exist")
                    raise Exception







source_0 = Sourcebutton(root, "source")

#kinter.messagebox.askokcancel(title=None, message=None, **options)

root.mainloop()