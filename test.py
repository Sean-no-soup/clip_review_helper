try: import vlc
except: print(" missing dependency https://pypi.org/project/python-vlc/")
import time


#one instance at a time: separate window
'''
media_player = vlc.MediaPlayer("video.mp4")
media_player.play()
time.sleep(5)
playing = set([1,2,3,4])
while True:
    state = media_player.get_state()
    if state not in playing:
        break'''




#window stays open, sometimes cant resize vertically while playing, how update media , \
# is there a way to get these in the same window?
import tkinter as tk
root=tk.Tk()
frame = tk.Frame(root, width=700, height=600)
frame.pack()
display = tk.Frame(frame, bd=5)
display.place(relwidth=1, relheight=1)

def onclick():
    print("clicked")
    p.set_media(instance.media_new("video2.mp4"))
    p.play()
    return

button = tk.Button(root, text="i forgot text",command=onclick)
button.pack()



instance=vlc.Instance()
p=instance.media_player_new()
m=instance.media_new("video.mp4")
#p.set_hwnd(root.winfo_id())
p.set_xwindow(display.winfo_id())
p.set_media(m)
p.play()


root.mainloop()
