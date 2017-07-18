from __future__ import print_function
import numpy as np

def quickSort(_A, _p, _r):
    if _p < _r:
        q = partition(_A, _p, _r)
        quickSort(_A, _p, q - 1)
        quickSort(_A, q + 1, _r)

def partition(_A, _p, _r):
    pivot = _A[_r]
    i = _p - 1
    for j in xrange(_p, _r, 1):
        if _A[j] <= pivot:
            i+=1
            x = _A[i]
            _A[i] = _A[j]
            _A[j] = x
    t = _A[_r]
    _A[_r] = _A[i + 1]
    _A[i + 1] = t
    return i+1

#while True:
rand_arr = np.random.randint(1000, 10000, 10)
print('Unsorted: ' + str(rand_arr) + '\n')
quickSort(rand_arr, 0, len(rand_arr) - 1)
print('Sorted: ' + str(rand_arr))

