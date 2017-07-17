import Tkinter as tk
import tkSimpleDialog as tksd

root = tk.Tk()

var = tksd.askfloat("title", "prompt")
print(var)
root.mainloop()