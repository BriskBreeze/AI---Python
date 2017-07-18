from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt # conda install matplotlib

myRange = np.random.rand(10000000)
mySum = 0

#for number in myRange:
#    mysum += number

mySum = myRange.sum()

print(mySum)

x = [1, 2, 4, 8]
y = [10, 40, 80, 20]

result = np.polyfit(x, y, 2)
eq = np.poly1d(result)

x2 = np.arange(-40, 90)
yfit = np.polyval(result, x2)

#print(yfit)

plt.plot(x, y, label = "Points")
plt.plot(x2, yfit, label = "Fit")
plt.savefig('example.png')

myString = '60.5'

number = 0
try:
    number = float(myString)
except ValueError:
    print('Not a float')
print(number)