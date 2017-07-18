from __future__ import print_function
import numpy as np
import Tkinter as tk
import tkMessageBox as tkmb
import tkSimpleDialog as tksd

import matplotlib.pyplot as plt # conda install matplotlib

def get_data(_step):
    angles = range(-40, 81, _step)
    distance = [65.3333, 99.6666, 130.0, 175.3333, 383.6666, 446.3333, 642.6666, 716.6666, 717.6666, 706.3333, 626.0, 636.3333, 365.3333, 0.0][::_step / 10]
    data = []
    data.append(angles)
    data.append(distance)
    return data

def get_distance(_angle, _data):
    result = np.polyfit(_data[0], _data[1], 6)
    eq = np.poly1d(result)
    x2 = np.arange(-40, 90)
    yfit = np.polyval(result, x2)
    plt.plot(_data[0], _data[1], label = "Points")
    plt.plot(x2, yfit, label = "Fir")
    if tkmb.askyesno("Save", "Would you like to save the graph?"):
        plt.savefig("Rocket Prediction.png")
    return eq(_angle)

def get_input():
    while True:  # get input
        var = tksd.askstring("Angle", "Please enter an angle (q to quit): ")
        try:
            return float(var)
        except ValueError:
            if var == 'q':
                exit(0)
            else:
                print("I'm sorry, you have entered an invalid angle.")

def render_frame():
    pass

root = tk.Tk()
cnv = tk.Canvas(root, width = 350, height = 200, bg = "lightgray")
cnv.create_text(20, 20, anchor = "nw", text = "Please enter an angle (\'q\' to quit)")

cnv.pack()
root.mainloop()

data = get_data(20)
'''while True: # continuous running
    angle = get_input()
    distance = get_distance(angle, data)
    print('\nDistance at an angle of ' + str(angle) + ' is: ' + str(distance), end = '\n\n')'''