#import mutagen
#import moviepy as mp
try: import vlc
except: print(" missing dependency https://pypi.org/project/python-vlc/")
import tkinter as tk
import tkinter.filedialog


root = tk.Tk()  # Create the main window
root.geometry("700x350")


class dirbutton(tk.Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(command = self.click_function, \
            width = "30", height = 2, borderwidth=2, relief="groove",\
            text="select directory")
        directory = ""

    def click_function(self):
        print("pressed button")
        path = tk.filedialog.askdirectory(mustexist=True)
        if path=="":
            return
        elif len(path) > 32:
            self.config(text=f"{path[:9]}...{path[-23:]}")
        else:
            self.config(text=path)

class dirlabel(tk.label):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(width = "30", height = 2, borderwidth=2, relief="groove")

testlbl1 = dirlabel(root, text="clips source")
testlbl1.grid(row=0, column=0, sticky="n")
testbtn1 = dirbutton(root)
testbtn1.grid(row=1, column=0, sticky="n")

testlbl2 = dirlabel(root, text="send clips to")
testlbl2.grid(row=0, column=1, sticky="n")
testbtn2 = dirbutton(root)
testbtn2.grid(row=1, column=1, sticky="n")

testlbl3 = dirlabel(root, text="dunno yet")
testlbl3.grid(row=0, column=2, sticky="n")
testbtn3 = dirbutton(root)
testbtn3.grid(row=1, column=2, sticky="n")





root.mainloop()