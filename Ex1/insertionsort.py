#!/usr/bin/python3


def swap(a, b):
    """

    >>> swap(1, 2)
    (2, 1)

    """
    temp = a
    a = b
    b = temp
    del temp
    return a, b


def insertionsort(lst):
    """ Sort list using the Insertion Sort algorithm.

    >>> insertionsort([24, 6, 12, 32, 18])
    [6, 12, 18, 24, 32]

    >>> insertionsort([])
    []

    >>> insertionsort("hallo")
    Traceback (most recent call last):
        ...
    TypeError: lst must be a list

    """
    # Check if lst is a list
    if not type(lst) == list:
        raise TypeError('lst must be a list')
    # For each element in lst
    for i in range(len(lst)-1):
        j = 0
        # print("i", i) # For debug purpose
        # Check if lst[i] needs to be moved and moves it through the list
        while (lst[i+1-j] < lst[i-j]) and (i-j >= 0):
            # print("j", j) # For debug purpose
            (lst[i+1-j], lst[i-j]) = swap(lst[i+1-j], lst[i-j])
            j += 1
            # print("lst", lst) # For debug purpose
    return lst


if __name__ == "__main__":
    # Create an unsorted list of integers.
    numbers = [10, 4, 1, 5, 2, 3, 11, 3, 9]
    # Sort the list.
    print(insertionsort(numbers))
