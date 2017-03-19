#!/usr/bin/python3

import argparse
import numpy as np

# Make function timeit globally available
from timeit import timeit 


class DynamicIntArray:
    """Dynamic integer array class implemented with fixed-size numpy array."""

    def __init__(self):
        """Create empty array with length 0 and capacity 1."""
        self._n = 0  # Number of elements in array
        self._c = 1  # Capacity
        self._a = self._create_array(self._c)

    def setarray(self, n, c, a):
        """Create empty array with length 0 and capacity 1."""
        self._n = n  # Number of elements in array
        self._c = c  # Capacity
        self._a = a

    def __len__(self):
        """Return number of elements in the array."""
        return self._n

    def __getitem__(self, i):
        """Return element at index i."""
        # Check for index out of bounds error.
        if not 0 <= i < self._n:
            raise IndexError('index out of bounds')

        return self._a[i]

    def size(self):
        """Return size of inner array."""
        return self._a.size

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
        """Remove integer value from end of array."""
        if self._n <= 1:
            return

        if self._n <= self._c // 3:  # time to resize
            self._resize(2 * self._n)

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


def test_1_or_2(append):
    """Test method for test 1 and 2."""
    size = 10000000  # Number of inserts / removes
    samples = 100  # 100 measure points

    # Use an inner function for the loop
    def appendFnc(n, array):
        for i in range(n):
            array.append(0)

    def removeFnc(n, array):
        for i in range(n):
            array.remove()

    arr = DynamicIntArray()
    if not append:  # Initialize array with 10 million elements
        for n in range(0, int(size)):
            arr.append(0)

    runtime = 0.0  # The total accumulated runtime
    factor = size // samples   # Number of steps per sample

    if append:
        def func():
            appendFnc(factor, arr)
    else:
        def func():
            removeFnc(factor, arr)

    for n in range(samples + 1):
        runtime += timeit(stmt=func, setup='import random', number=1)
        print('%d\t%.5f' % (n * factor, runtime))


def test_3_or_4(do_append):
    """Test method for test 3 and 4."""
    size = 10000000  # Number of inserts / removes
    initial_size = 1000000  # Number of initial elements
    samples = 100  # 100 measure points

    # Use an inner function for the loop
    def testFnc(n, array, append):
        last_size = array.size()
        for i in range(n):
            if append[0]:
                array.append(0)
            else:
                array.remove()

            # Update append / remove
            new_size = array.size()
            append[0] ^= (last_size != new_size)
            last_size = new_size

    runtime = 0.0  # The total accumulated runtime
    factor = size // samples  # Number of steps per sample
    append = [do_append]

    # Initialize array with 1 million elements
    arr = DynamicIntArray()
    for n in range(0, initial_size):
        arr.append(0)

    for n in range(samples + 1):
        runtime += timeit(stmt=lambda: testFnc(factor, arr, append), number=1)
        print('%d\t%.5f' % (n * factor, runtime))


if __name__ == '__main__':
    # Parse the arguments and execute the selected tests
    parser = argparse.ArgumentParser()
    parser.add_argument('-t1', action='store_true')
    parser.add_argument('-t2', action='store_true')
    parser.add_argument('-t3', action='store_true')
    parser.add_argument('-t4', action='store_true')

    args = parser.parse_args()
    if args.t1:
        # Use an empty array and append 10 million elements
        print('Test 1:')
        test_1_or_2(True)

    if args.t2:
        # Use an array with 10 million elements and remove 10 million elements
        print('Test 2:')
        test_1_or_2(False)

    if args.t3:
        # Use an array with 1 million elements and append / remove elements
        # until the next reallocation occurs. The test starts with append.
        print('Test 3:')
        test_3_or_4(True)

    if args.t4:
        # Use an array with 1 million elements and append / remove elements
        # until the next reallocation occurs. The test starts with remove.
        print('Test 4:')
        test_3_or_4(False)
