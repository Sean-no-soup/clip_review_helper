import tkinter as tk
import tkinter.filedialog
from os import listdir
import dbm #unix database interface
try: import vlc
except AssertionError: print(" missing dependency https://pypi.org/project/python-vlc/")

root = tk.Tk()  # Create the main window
root.geometry("700x350")
global source
source = ""

class Dirbutton(tk.Frame):
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

    directory = ""

    def click_function(self):
        dirpath = tk.filedialog.askdirectory(mustexist=True)
        if dirpath=="":return
        self.directory = dirpath

        if len(dirpath) > 32: #long directory check and display format
            self.button.config(text=f"{dirpath[:9]}...{dirpath[-23:]}")
        else:
            self.button.config(text=dirpath)

class Sourcebutton(Dirbutton):
    directory = ""
    fileList = []
    index = 0

    def click_function(self): #select directory
        dirpath = tk.filedialog.askdirectory(mustexist=True)
        if dirpath=="":return
        self.directory = dirpath
        global source
        source = dirpath

        if len(dirpath) > 32: #long directory check and display format
            self.button.config(text=f"{dirpath[:9]}...{dirpath[-23:]}")
        else:
            self.button.config(text=dirpath)

        for file in listdir(dirpath):
            if file.endswith(".mp4"):
                self.fileList.append(file)
        
    def gonext():
        self.index +=1
        player.set_media(Instance.media_new(fileList[index]))
        player.play()
    
    def golast():
        self.index -=1
        player.set_media(Instance.media_new(fileList[index]))
        player.play()

class PlayerControls(tk.Frame):
    def __init__(self, parent):
        super().__init__(master = parent)
        self.rowconfigure(0, weight = 1, uniform='a')
        self.columnconfigure((0,1,2,3,4), weight = 1, uniform='a')
        self.label1 = tk.Label(self, text = '1-4: move to bin', bg="grey")
        self.label1.grid(row = 0, column = 0, sticky = 'nsew')
        self.label2 = tk.Label(self, text = 'space: toggle play', bg="grey")
        self.label2.grid(row = 0, column = 1, sticky = 'nsew')
        self.label3 = tk.Label(self, text = '(shift)enter:play next(last)', bg="grey")
        self.label3.grid(row = 0, column = 2, sticky = 'nsew')
        self.label4 = tk.Label(self, text = 'left/right:seek 5s', bg="grey")
        self.label4.grid(row = 0, column = 3, sticky = 'nsew')
        self.label4 = tk.Label(self, text = 'up/down: note/kill', bg="grey")
        self.label4.grid(row = 0, column = 4, sticky = 'nsew')
        self.pack(expand = False, fill = tk.X, side=tk.TOP)

controls = PlayerControls(root)

playerframe = tk.Frame(root, bg="green", width=50, height=50)
playerframe.pack(expand=1, fill=tk.BOTH, side=tk.TOP)
Instance=vlc.Instance()
player=Instance.media_player_new()
player.set_hwnd(playerframe.winfo_id()) # yes I know this will not work on some computers, TOO BAD 

source = Sourcebutton(root, "source")
button_1 = Dirbutton(root, "bin 1")
button_2 = Dirbutton(root, "bin 2")
button_3 = Dirbutton(root, "bin 3")
button_4 = Dirbutton(root, "bin 4")

#db = dbm.open('queued changes','c') #open database, creating it if necessary
#db.get('key_name)
#db['key'] = 'value_string'
# for key, value in db.items():
#     print(key, value)zz

root.bind("1", lambda x: print("You pressed 1"))
root.bind("2", lambda x: print("You pressed 2"))
root.bind("3", lambda x: print("You pressed 3"))
root.bind("4", lambda x: print("You pressed 4"))
root.bind("<space>", lambda x: print("You pressed space"))
root.bind("<Left>", lambda x: print("You pressed left"))
root.bind("<Right>", lambda x: print("You pressed right"))
root.bind("<Up>", lambda x: print("You pressed up"))
root.bind("<Down>", lambda x: print("You pressed down"))
root.bind("<Return>", lambda x: print("You pressed enter"))
root.bind("<Shift-Return>", lambda x: print("You pressed shift+enter"))

root.mainloop()