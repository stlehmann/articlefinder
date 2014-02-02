import tkinter

root = tkinter.Tk()
s = tkinter.Scrollbar(root)
T = tkinter.Text(root)

T.focus_set()
s.pack(side=tkinter.RIGHT, fill=tkinter.Y)
T.pack(side=tkinter.LEFT, fill=tkinter.Y)
s.config(command=T.yview)
T.config(yscrollcommand=s.set)

for i in range(40):q
   T.insert(tkinter.END, "This is line %d\n" % i)
   T.yview(tkinter.MOVETO, 1.0)

tkinter.mainloop()