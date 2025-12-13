





def onclick():
    print("clicked")
    p.set_media(Instance.media_new("video2.mp4"))
    p.play()
    return

frame = tk.Frame(root)
frame.pack(expand=1, fill=tk.BOTH)

button = tk.Button(root, text="open video2",command=onclick)
button.pack()

Instance=vlc.Instance()
p=Instance.media_player_new()
m=Instance.media_new("video.mp4")
p.set_hwnd(frame.winfo_id()) # yes I know this will not work on some computers, TOO BAD 
p.set_media(m)
p.play()

root.mainloop()