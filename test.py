from Tkinter import *
import tkMessageBox
import Tkinter


top = Tkinter.Tk()

def helloCallBack():
   B.place(x=20, y=20)

B = Tkinter.Text(top)

B.pack()
B.place(bordermode=OUTSIDE, height=100, width=100)
top.mainloop()
