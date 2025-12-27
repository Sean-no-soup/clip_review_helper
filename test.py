import vlc
import tkinter as tk

root = tk.Tk()  # Create the main window
root.geometry("700x350")

Instance=vlc.Instance(r"--sout-all --sout #display %1%")
player=Instance.media_player_new()
player.set_hwnd(root.winfo_id())

path = "video2.mp4" #temporary file
player.set_media(Instance.media_new(path))
player.play()

root.mainloop()