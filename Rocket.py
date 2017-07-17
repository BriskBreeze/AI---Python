from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt # conda install matplotlib

def get_training_data(_distance):
    angles = range(-40, 81, 20) # gets list of angles
    dist = _distance[::2] # gets list of distances given angle freq
    data = [] # empty list for data points
    data.append(angles) # adds angles
    data.append(dist) # adds distances
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

def MAE(_test_set):
    n = len(_test_set)
    sum = 0.0
    for i in xrange(n):
        sum += AE(_test_set[0][i], _test_set[1][i])
    #print(sum)
    return sum / n

def MSE(_test_set):
    n = len(_test_set)
    sum = 0.0
    for i in xrange(n):
        sum += AE(_test_set[0][i], _test_set[1][i]) ** 2
    return sum / n

def RMSD(_test_set):
    return MSE(_test_set) ** 1/2

def AE(_n1, _n2):
    return abs(_n1 - _n2)

test_set = [[100.0, 98.0, 4.0, 3.0], [100.0, 100.0, 0.0, 5.0]]
print(MAE(test_set))

distance = [65.3333, 99.6666, 130.0, 175.3333, 383.6666, 446.3333, 642.6666, 716.6666, 717.6666, 706.3333, 626.0, 636.3333, 365.3333, 31.6666]
data = get_training_data(distance) # loads data
while True: # continuous running
    pass
    #angle = get_input() # gets user input
    #distance = get_distance(angle, data) # calculates distance given angle
    #print('\nDistance at an angle of ' + str(angle) + ' is: ' + str(distance), end = '\n\n') # outputs distance
