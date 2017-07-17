from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt # conda install matplotlib

def get_data(_step):
    angles = range(-40, 81, _step) # gets list of angles
    distance = [65.3333, 99.6666, 130.0, 175.3333, 383.6666, 446.3333, 642.6666, 716.6666, 717.6666, 706.3333, 626.0, 636.3333, 365.3333, 0.0][::_step / 10] # gets list of distances given angle freq
    data = [] # empty list for data points
    data.append(angles) # adds angles
    data.append(distance) # adds distances
    return data

def get_distance(_angle, _data):
    result = np.polyfit(_data[0], _data[1], 6) # makes poly data
    eq = np.poly1d(result) # builds equation
    x2 = np.arange(-40, 90) # sets range
    yfit = np.polyval(result, x2) # gets y vals for range of x
    plt.plot(_data[0], _data[1], label = "Points") # plots the points
    plt.plot(x2, yfit, label = "Fit") # plots the fit line
    plt.savefig("Rocket Prediction.png") # saves image
    return eq(_angle) # returns the distance

def get_input():
    while True:  # get input
        input = raw_input("Please enter an angle (q to quit): ") # gets text input
        try:
            return float(input) # tries parsing to a float
        except ValueError:
            if input == 'q': # quit on q
                exit(0)
            else: # default message
                print("I'm sorry, you have entered an invalid angle.")


data = get_data(20) # loads data
while True: # continuous running
    angle = get_input() # gets user input
    distance = get_distance(angle, data) # calculates distance given angle
    print('\nDistance at an angle of ' + str(angle) + ' is: ' + str(distance), end = '\n\n') # outputs distance
