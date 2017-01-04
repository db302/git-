#!/usr/bin/env python # changed from python3 to python, as in makefile
import time
import random as rnd
# import numpy as np
# import scipy as sp
# import matplotlib as mlp
import matplotlib.pyplot as plt
from pylab import ion  # changed from * to ion due to flake8 violation
# import random
# Position of this import randon statement is relevant!
# Multiple definition of "random"? Seems to have a different definitions in
# pylab... Why does the Python interpreter not produce a warning? Import
# statement modified imported "as rnd" -> solution see line 3
#
# What is the difference between '' and ""? -No difference?


def heapsort(lst):
    """ Sorts a list using the Heapify algorithm.

    >>> heapsort([10, 4, 1, 5, 2, 3, 11, 3, 9, 20])
    [1, 2, 3, 3, 4, 5, 9, 10, 11, 20]

    >>> heapsort([])
    []

    >>> heapsort("hallo")
    Traceback (most recent call last):
        ...
    TypeError: lst must be a list

    """
    # Check if lst is a list
    if not type(lst) == list:
        raise TypeError('lst must be a list')
    heapify(lst)
    # print(lst)
    for i in range(len(lst)-1):
        # print(i)
        (lst[0], lst[len(lst)-1-i]) = (lst[len(lst)-1-i], lst[0])
        # print(lst)
        repair_heap(lst, 0, len(lst)-i-1)
        # print(lst)
    # print("Sorting finished")
    return(lst)


def heapify(lst):
    """ Generates a Max Heap using the Heapify algorithm.

    >>> heapify([10, 4, 1, 5, 2, 3, 11, 3, 9, 20]) # Even elements
    [20, 10, 11, 9, 4, 3, 1, 3, 5, 2]

    >>> heapify([10, 4, 1, 5, 2, 3, 11, 3, 9, 20, 30]) # Odd elements
    [30, 20, 11, 9, 10, 3, 1, 3, 5, 4, 2]

    >>> heapify([])
    []

    >>> heapify("hallo")
    Traceback (most recent call last):
        ...
    TypeError: lst must be a list

    """
    # Check if lst is a list
    if not type(lst) == list:
        raise TypeError('lst must be a list')
    for i in range((int)(len(lst)/2-1), -1, -1):
        repair_heap(lst, i, len(lst))
    return lst


def repair_heap(lst, start_index, heap_size):
    """ Repairs a Max Heap

    >>> repair_heap([20, 3, 11, 10, 4, 3, 1, 9, 5, 2], 1, 10) # Even elements
    [20, 10, 11, 9, 4, 3, 1, 3, 5, 2]

    # Odd elements
    >>> repair_heap([4, 30, 11, 9, 20, 3, 1, 3, 5, 10, 2], 0, 11)
    [30, 20, 11, 9, 10, 3, 1, 3, 5, 4, 2]

    >>> repair_heap([], 0, 0)
    []

    >>> repair_heap("hallo", 0, 0)
    Traceback (most recent call last):
        ...
    TypeError: lst must be a list

    """
    # Check if lst is a list
    if not type(lst) == list:
        raise TypeError('lst must be a list')
    if heap_size > 1:
        # print(start_index)
        # print(lst)
        l_child_index = 2*start_index+1
        r_child_index = 2*start_index+2
        if r_child_index >= heap_size:  # not very nice...
            r_child_index = l_child_index
        if (lst[start_index] < lst[l_child_index] or
                lst[start_index] < lst[r_child_index]):
            if lst[r_child_index] >= lst[l_child_index]:
                (lst[start_index], lst[r_child_index]) = (lst[r_child_index],
                                                          lst[start_index])
                if r_child_index <= heap_size/2-1:
                    repair_heap(lst, r_child_index, heap_size)
            else:
                (lst[start_index], lst[l_child_index]) = (lst[l_child_index],
                                                          lst[start_index])
                if l_child_index <= heap_size/2-1:
                    repair_heap(lst, l_child_index, heap_size)
    # print(lst)
    return(lst)


def gen_rand_list(lst, length, lowVal, highVal):
    """ Generates a list with length and values between lowVal, highVal

    >>> res = gen_rand_list([], 10, 2, 5)
    >>> all([2 <= val <= 5 for val in res])
    True

    >>> gen_rand_list([], 0, 0, 1)
    []

    >>> gen_rand_list([], 0, 1, 0)
    Traceback (most recent call last):
    ...
    ValueError: highVal must be grater then lowValue

    >>> gen_rand_list("hallo", 0, 0, 1)
    Traceback (most recent call last):
        ...
    TypeError: lst must be a list

    """
    if not type(lst) == list:
        raise TypeError('lst must be a list')
    if not highVal > lowVal:
        raise ValueError('highVal must be grater then lowValue')
    for i in range(length):
        # lst.append(random.randrange(0, 10000, 1))
        lst.append(rnd.randrange(lowVal, highVal, 1))
    return lst


if __name__ == "__main__":
    # Parameter for ploting
    USE_SAME_LIST_IN_REPETITION = 0
    repetition = 2
    N = [10, 50, 100, 250, 500, 1000, 2500, 5000, 10000, 25000, 50000, 100000]
    OutputFileName = 'runtimeplot'
    ShowPlot = 1
    # Sort the list.
    runtime = []
    legend = []
    runtimeAvg = list(0 for i in range(len(N)))
    # print(runtimeAvg)
    for i in range(len(N)):
        lst = []
        if USE_SAME_LIST_IN_REPETITION:
            gen_rand_list(lst, N[i], 0, 10000)
        # print(len(lst))
        # print(N[i])
        for j in range(repetition):
            if not USE_SAME_LIST_IN_REPETITION:
                gen_rand_list(lst, N[i], 0, 10000)
            tic = time.time()
            heapsort(lst)
            toc = time.time()
            # print(toc - tic)
            runtime.append(toc - tic)
        # print(lst)
    # print(runtime)
    # runtime=list([0.9,1.0,1.5,1.9,2.1,2.0,])
    # print(runtime)
    if ShowPlot:
        ion()  # Switch to interactive mode
    for k in range(repetition):
        # print("k ", k)
        # print(runtime[k::repetition])
        plt.plot(runtime[k::repetition], N)
    for l in range(len(N)):
        # print("l ", l)
        runtimeAvg[l] = sum(runtime[l*repetition:(l+1)*(repetition)])
        # print("Avg", runtimeAvg)
    # print(repetition)
    runtimeAvg = [x/repetition for x in runtimeAvg]
    # print(runtimeAvg)
    plt.plot(runtimeAvg, N)
    legend = list("Run {0}".format(m) for m in range(repetition))
    legend.append("Avg")
    plt.legend(legend, loc='best')
    if USE_SAME_LIST_IN_REPETITION:
        plt.title('Runtime Plot - Same Data')
    else:
        plt.title('Runtime Plot - Different Data')
    plt.xlabel("Execution time [s]")
    plt.ylabel("Length of list")
    plt.savefig(OutputFileName, dpi=300)
    if ShowPlot:
        plt.show  # Shows the plot in a figure window
        # Wait for enter to finish script and close figure window
        # real_raw_input somehow redefined for raw_input due to get flake8 pass
        # Some python2/3 issue? I do not understand...
        real_raw_input = vars(__builtins__).get('raw_input', input)
        real_raw_input("Press enter to continue")
