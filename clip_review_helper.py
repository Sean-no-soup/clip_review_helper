import tkinter as tk
import tkinter.filedialog
from os import listdir
import dbm #unix database interface
try: import vlc
except AssertionError: print(" missing dependency https://pypi.org/project/python-vlc/")

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
        if num==0 and not force_play:
            player.pause()
        else:
            self.index = (self.index+num)%(self.num_files)
            path = f"{self.directory}{self.fileList[self.index]}"
            player.set_media(Instance.media_new(path))
            player.play()


    def click_function(self): #select directory
        dirpath = tk.filedialog.askdirectory(mustexist=True).replace("/","\\")+"\\"
        if dirpath=="":return
        color_selected(0) #highlight source
        self.directory = dirpath

        if len(dirpath) > 32: #long directory check and display format
            self.button.config(text=f"{dirpath[:9]}...{dirpath[-23:]}")

        else:
            self.button.config(text=dirpath)

        for file in listdir(dirpath):
            if file.endswith(".mp4"):
                self.fileList.append(file)
                self.num_files += 1
        
        self.playnext(force_play=True)


'''
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
'''

def color_selected(select_bin=0):

    '''set colors of bins to represent a queued move. 
    relies on global bin_list. select -1 to show delete'''

    global bin_list

    for _bin in bin_list:
        _bin.label.configure(bg="grey")

    if select_bin==-1:
        bin_list[0].label.configure(bg="#ED593B")
        return

    else:
        bin_list[select_bin].label.configure(bg="#3B5CED")
        return

#notes/buttons about controls at top
#controls = PlayerControls(root)

#main window
playerframe = tk.Frame(root, bg="green", width=50, height=50)
playerframe.pack(expand=1, fill=tk.BOTH, side=tk.TOP)
Instance=vlc.Instance()
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


#TODO : store queued changes in bound functions
#db = dbm.open('queued changes','c') #open database, creating it if necessary
#db.get('key_name)
#db['key'] = 'value_string'
# for key, value in db.items():
#     print(key, value)zz


#bind queue bins todo
root.bind('<Escape>', lambda x: color_selected(0))
root.bind("1", lambda x: color_selected(1))
root.bind("2", lambda x: color_selected(2))
root.bind("3", lambda x: color_selected(3))
root.bind("4", lambda x: color_selected(4))

#bind queue delete
root.bind("<Down>", lambda x: color_selected(-1))

#bind next, last, play, pause
root.bind("<space>", lambda x: source_0.playnext(0))
root.bind("<Left>", lambda x: source_0.playnext(-1))
root.bind("<Right>", lambda x: source_0.playnext(1))


# root.bind("<Up>", lambda x: print("You pressed up"))

# root.bind("<Return>", lambda x: print("You pressed enter"))
# root.bind("<Shift-Return>", lambda x: print("You pressed shift+enter"))

root.mainloop()