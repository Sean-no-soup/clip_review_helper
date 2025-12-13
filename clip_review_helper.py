import tkinter as tk
import tkinter.filedialog
try: import vlc
except: print(" missing dependency https://pypi.org/project/python-vlc/")

root = tk.Tk()  # Create the main window
root.geometry("700x350")


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
        print("pressed button")
        dirpath = tk.filedialog.askdirectory(mustexist=True)
        if dirpath=="":return
        self.directory = path

        if len(dirpath) > 32: #long directory check and display format
            self.button.config(text=f"{dirpath[:9]}...{dirpath[-23:]}")
        else:
            self.button.config(text=dirpath)


class Player_Controls(tk.Frame):
        def __init__(self, parent):
            super().__init__(master = parent)
            
        def onclick(): #play new media placeholder
            p.set_media(Instance.media_new("video2.mp4"))
            p.play()
            return

class Canvas(tk.Frame):
    def __init__(self, parent):
        super().__init__(master = parent)

frame = tk.Frame(root, bg="green", width=50, height=50)
frame.pack(expand=1, fill=tk.BOTH, side=tk.TOP)

Dirbutton(root, "source")
Dirbutton(root, "bin 1")
Dirbutton(root, "bin 2")
Dirbutton(root, "bin 3")



Instance=vlc.Instance()
p=Instance.media_player_new()
m=Instance.media_new("video.mp4")
p.set_hwnd(frame.winfo_id()) # yes I know this will not work on some computers, TOO BAD 
p.set_media(m)
p.play()

root.mainloop()



root.mainloop()