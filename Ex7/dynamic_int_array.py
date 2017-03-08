#!/usr/bin/python3

import argparse
import numpy as np
import timeit
import random
import math


class DynamicIntArray:
    """Dynamic integer array class implemented with fixed-size numpy array."""

    def __init__(self):
        """Create empty array with length 0 and capacity 1."""
        self._n = 0  # Number of elements in array
        self._c = 1  # Capacity
        self._a = self._create_array(self._c)

    def __len__(self):
        """Return number of elements in the array."""
        return self._n

    def __getitem__(self, i):
        """Return element at index i."""
        # Check for index out of bounds error.
        if not 0 <= i < self._n:
            raise IndexError('index out of bounds')
        return self._a[i]

    def append(self, value):
        """Add integer value to end of array."""
        # Check if given value is of integer type.
        if not isinstance(value, int):
            raise TypeError('value is not integer')
        if self._n == self._c:  # time to resize
            self._resize(2 * self._c)
        self._a[self._n] = value
        self._n += 1

    def remove(self):
        """ Remove the last element form the array. """
        if not self._c > 0:
            raise IndexError('index out of bound')
        if self._n < math.floor(float(self._c/3)):
            self._resize(math.floor(self._n*2))
        self._n -= 1

    def _resize(self, new_c):
        """Resize array to capacity new_c."""
        b = self._create_array(new_c)
        for i in range(self._n):
            b[i] = self._a[i]
        # Assign old array reference to new array.
        self._a = b
        self._c = new_c

    def _create_array(self, new_c):
        """Return new array with capacity new_c."""
        return np.empty(new_c, dtype=int)  # data type = integer


def test1():
    a = DynamicIntArray()
    tic = timeit.default_timer()
    for i in range(int(10e6)):
        a.append(random.randint(0, 1000))
        toc = timeit.default_timer()
        print(str(i) + "\t" + str(toc - tic))


def test2():
    a = DynamicIntArray()
    for i in range(int(10e6)):
        a.append(random.randint(0, 1000))
    tic = timeit.default_timer()
    for i in range(len(a)):
        a.remove()
        toc = timeit.default_timer()
        print(str(i) + "\t" + str(toc - tic))


def test3():
    a = DynamicIntArray()
    for i in range(int(1e6)):
        a.append(random.randint(0, 1000))
    tic = timeit.default_timer()
    arrayId = id(a._a)
    toggle = 0
    for i in range(int(10e6)):
        if toggle == 0:
            a.append(random.randint(0, 1000))
            if id(a._a) != arrayId:
                toggle = 1
        else:
            a.remove()
            if id(a._a) != arrayId:
                toggle = 0
        toc = timeit.default_timer()
        print(str(i) + "\t" + str(toc - tic))


def test4():
    a = DynamicIntArray()
    for i in range(int(1e6)):
        a.append(random.randint(0, 1000))
    tic = timeit.default_timer()
    arrayId = id(a._a)
    toggle = 1  # start with remove()
    for i in range(int(10e6)):
        if toggle == 0:
            a.append(random.randint(0, 1000))
            if id(a._a) != arrayId:
                toggle = 1
        else:
            a.remove()
            if id(a._a) != arrayId:
                toggle = 0
        toc = timeit.default_timer()
        print(str(i) + "\t" + str(toc - tic))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--Test1", help="Runs Test 1", action="store_true")
    parser.add_argument("--Test2", help="Runs Test 2", action="store_true")
    parser.add_argument("--Test3", help="Runs Test 3", action="store_true")
    parser.add_argument("--Test4", help="Runs Test 4", action="store_true")
    args = parser.parse_args()
    if args.Test1:
        test1()
    if args.Test2:
        test2()
    if args.Test3:
        test3()
    if args.Test4:
        test4()
