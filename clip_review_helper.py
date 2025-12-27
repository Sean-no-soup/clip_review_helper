import tkinter as tk
import tkinter.filedialog
import tkinter.simpledialog
import os
import dbm
import vlc #dependency https://pypi.org/project/python-vlc/

root = tk.Tk()  # Create the main window
root.geometry("700x350")

class Header(tk.Frame):
    def __init__(self, parent, comment="<comment>", file_name="<file name>", move_to="<move to>"):
        super().__init__(master = parent)
        self.rowconfigure(0, weight = 1, uniform='a')
        self.columnconfigure((0,1,2), weight = 1, uniform='a')
        self.comment = tk.Label(self, text = comment, bg="grey")
        self.comment.grid(row = 0, column = 0, sticky = 'nsew')
        self.file_name = tk.Label(self, text = file_name, bg="grey")
        self.file_name.grid(row = 0, column = 1, sticky = 'nsew')
        self.move_to = tk.Label(self, text = move_to, bg="grey")
        self.move_to.grid(row = 0, column = 2, sticky = 'nsew')
        self.pack(expand = False, fill = tk.X, side=tk.TOP)

    def update(self):
        move, comment = source_0.update_db() #no flag= check only

        if move not in "-101234":
            self.move_to.configure(text=f"move to...{move[-15:]}")
            color_selected(None)
            for i in range(len(bin_list)):
                if move == bin_list[i].directory:
                    color_selected(i)

        elif move == "0":
            self.move_to.configure(text="don't move")
            color_selected(0)

        elif move == "-1":
            self.move_to.configure(text="delete")
            color_selected(-1)

        elif move in "1234": #should be redundant
            self.move_to.configure(text=f"move to bin {move}")
            color_selected(int(move))

        else:
            print(f"error updating header with move {move}")

        move = move[-20:]
        file_name = source_0.fileList[source_0.index][-35:-4]

        self.comment.configure(text = comment)
        self.file_name.configure(text = file_name)

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
        if dirpath=="":return
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

    def playnext(self, num=1, force_play:bool=False):
        if num==0 and not force_play: #pause/resume
            player.pause()
        else: #start playing a file, update feedback from db
            self.index = (self.index+num)%(self.num_files)
            path = f"{self.directory}{self.fileList[self.index]}"
            player.set_media(Instance.media_new(path))
            player.play()
            myheader.update()

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
        
        self.playnext(force_play=True)

    def update_db(self, flag="", value=""):
        dbpath = f'{self.directory}\\queued cache'
        key =self.fileList[self.index]
        with dbm.open(dbpath, 'c') as db:

            try: 
                move,comment = db[key].decode("utf-8").split("::")
            except:
                db[key] = "0::"
                move,comment = "0::".split("::")

            if flag == "comment":
                db[key] = f"{move}::{value}"

            elif flag == "move":
                db[key] = f"{value}::{comment}"


            print (db[key].decode("utf-8").split("::"))
            return (db[key].decode("utf-8").split("::")) #returns (move, comment)
    
def color_selected(select_bin=0):

    '''set colors of bins to represent a queued move. 
    relies on global bin_list. select -1 to show delete'''

    for _bin in bin_list:
        _bin.label.configure(bg="grey")

    if select_bin == None:
        return

    if select_bin==-1:
        bin_list[0].label.configure(bg="#ED593B")
        return

    else:
        bin_list[select_bin].label.configure(bg="#3B5CED")
        return

def update_move(num):
    if num == 0:
        source_0.update_db(flag="move", value="0")
        print("dont move")
        
    elif num == -1:
        source_0.update_db(flag="move", value="-1")
        print("delete")

    else:
        move_to_path = bin_list[num].directory
        if move_to_path == "":
            bin_list[num].click_function() #select directory
            print("no directory in that bin")
            return
        else:
            source_0.update_db(flag="move", value=move_to_path)
            print(f"move to {move_to_path}")

    myheader.update()

def update_comment():
    commentstr = tkinter.simpledialog.askstring(title="",prompt="comment?")
    source_0.update_db(flag="comment", value=commentstr)
    myheader.update()

#comment and file name
myheader = Header(root)

#main window
playerframe = tk.Frame(root, bg="green", width=50, height=50)
playerframe.pack(expand=1, fill=tk.BOTH, side=tk.TOP)
Instance=vlc.Instance() #"--sout-all","--sout #display %1%")
player=Instance.media_player_new()
player.set_hwnd(playerframe.winfo_id()) # yes I know this will not work on some computers, TOO BAD 

#buttons at bottom
source_0 = Sourcebutton(root, "source")
button_1 = Dirbutton(root, "bin 1")
button_2 = Dirbutton(root, "bin 2")
button_3 = Dirbutton(root, "bin 3")
button_4 = Dirbutton(root, "bin 4")

#more setup that could probably be better thought out
global bin_list
bin_list = [source_0,button_1,button_2,button_3,button_4]

#bind queue delete
root.bind("<Down>", lambda x: update_move(-1))

#bind queue bins todo
root.bind('<Escape>', lambda x: update_move(0))
root.bind("1", lambda x: update_move(1))
root.bind("2", lambda x: update_move(2))
root.bind("3", lambda x: update_move(3))
root.bind("4", lambda x: update_move(4))

#add comment
root.bind("<Up>", lambda x: update_comment()) #temp

#bind next, last, play, pause
root.bind("<space>", lambda x: source_0.playnext(0))
root.bind("<Left>", lambda x: source_0.playnext(-1))
root.bind("<Right>", lambda x: source_0.playnext(1))

root.bind("<Return>", lambda x: print()) #terminal convenience

root.mainloop()