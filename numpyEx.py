from __future__ import print_function
import numpy as np
from numpy.linalg import inv

ones = np.ones(4)
onesM = np.ones((3, 4))

onesM[0][0] = 2
ones[2] = 0

ones *= 4
onesM *= ones

print(onesM)
#rows = 1
print(onesM.sum(axis=1))
#cols = 0
print(onesM.sum(axis=0))

randomM = np.random.rand(3,3) * 10
randomM[2, 2] = 11
randomM[1, :] = 2
randomM[:, 2] = 3
randomM **= -1

rndMinv = inv(randomM)
print(randomM)
print(rndMinv)