from __future__ import print_function
import numpy as np

arr1 = np.ones((5, 4))
arr2 = np.zeros(4)
arr2[0] = 1
print(arr1 * arr2)
arr1[1, 2] = 10
arr1 *= 2
print(arr1)
print(arr1.sum())
print(arr1.max(axis=1))
print(arr1.mean(axis=0))
