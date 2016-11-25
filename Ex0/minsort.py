#!/usr/bin/python3


def minsort(lst):
    """ Sort list using the MinSort algorithm.

    >>> minsort([24, 6, 12, 32, 18])
    [6, 12, 18, 24, 32]

    >>> minsort([])
    []

    >>> minsort("hallo")
    Traceback (most recent call last):
        ...
    TypeError: lst must be a list

    """
    # Check given parameter data type.
    if not type(lst) == list:
        raise TypeError('lst must be a list')

    # Get length of the list.
    n = len(lst)
    # For each list element.
    for i in range(n):
        # Find the minimum in list[i..n-1].
        min_value = lst[i]
        min_index = i
        for j in range(i + 1, n):
            if lst[j] < min_value:
                min_value = lst[j]
                min_index = j
        # Swap minimum to position i.
        lst[i], lst[min_index] = lst[min_index], lst[i]

    return lst


if __name__ == "__main__":
    # Create an unsorted list of integers.
    numbers = [10, 4, 1, 5, 2, 3, 11, 3, 9]
    # Sort the list.
    print(minsort(numbers))
