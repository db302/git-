#!/usr/bin/env python3
import random as rnd
# import time
import timeit
import sys
sys.setrecursionlimit(2**17)


def generate_list_of_random_nbr(n):
    """ Generates a list of n random numbers in range 1..n
        n:  length of the list
    >>> res = generate_list_of_random_nbr(10)
    >>> all([1 <= val <= 10 for val in res])
    True
    """
    lst = []
    rnd.seed()  # None
    for i in range(n):
        lst.append(rnd.randint(1, n))
    return lst


def quicksort(lst, start, stopp):
    """ Sorts a list using quicksort algorithm
        lst:    list to sort
        start:  index of the first element in the list
        stopp:  index of the last element in the list
    >>> l = list([10, 8, 2, 1, 7, 9, 5, 4, 3, 6])
    >>> quicksort(l, 0, len(l) - 1)
    >>> print(l)
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    """
    if not type(lst) == list:
        raise TypeError("lst must be a list")
    if start > len(lst) or stopp > len(lst):
        raise IndexError("start or stopp out of bounce")
    if (stopp - start) < 1:
        return
    i = start
    k = stopp
    pivot = lst[start]
    # print(pivot)
    while k > i:
        while lst[i] <= pivot and i <= stopp and k > i:
            i += 1
        while lst[k] > pivot and k >= start and k >= i:
            k -= 1
        if k > i:
            (lst[i], lst[k]) = (lst[k], lst[i])
    (lst[start], lst[k]) = (lst[k], lst[start])
    # print(lst)
    quicksort(lst, start, k - 1)
    quicksort(lst, k + 1, stopp)


# Copied from Exercise Sheet 5
# Start>>>
class HashFunction:
    """ Class for implementing a Hashtable
        h_(a, b) = ((a * x) + b) mod p) mod m
    """
    def __init__(self, p, u, m, a=None, b=None):
        """ Constructor for class HashTable
            p:      prime number, hash function parameter
            u:      universe size
            m:      hash table size
            a, b:   hash function parameter
        """
        # if not p > m:
        #    raise ValueError("p must be greater then m")
        # if not p > u:
        #    raise ValueError("p must be greater then u")
        self.a = a
        self.b = b
        self.p = p
        self.u = u
        self.m = m
        self.hashtable = []
        for i in range(m):
            self.hashtable.append([])

    def apply(self, x):
        """ Puts value in Hashtable
            x:      >Value
        """
        if (self.a is not None) and (self.b is not None):
            index = ((self.a * x + self.b) % self.p) % self.m
            self.hashtable[index].append(x)
            return index

    def set_random_parameters(self):
        """ Sets random parameters a, b """
        self.a = rnd.randrange(1, self.p - 1, 1)
        self.b = rnd.randrange(0, self.p - 1, 1)
# Copied from Exercise Sheet 5
# <<<Stop

    def add_list(self, lst):
        """ Adds all values of a list into the hashtable
            lst:    List to put into the hastable
        """
        for i in range(len(lst)):
            self.apply(lst[i])
        # print self.hashtable

    def clear_table(self):
        """ Generates a new hashtable with the existing parameters """
        self.hashtable = []
        for i in range(self.m):
            self.hashtable.append([])

    def get_table_entry_count(self):
        """ Counts all elements in the hashtable """
        count = 0
        for i in range(self.m):
            for j in range(len(self.hashtable[i])):
                count += 1
        return count


def calculate_runtime(n, hash_p, hash_u, hash_m):
    lst = generate_list_of_random_nbr(n)
    h = HashFunction(hash_p, hash_u, hash_m)
    h.set_random_parameters()
    runtime_quicksort = 0
    runtime_hashtable = 0
    for i in range(3):
        # tic = time.timer()
        runtime_quicksort += timeit.timeit(stmt=lambda:
                                           quicksort(lst, 0,
                                                     len(lst) - 1),
                                           number=1)
        # toc = time.timer()
        # runtime_quicksort += toc - tic
        h.clear_table()
        # print(str(h.get_table_entry_count()))  # for test
        # tic = time.timer()
        runtime_hashtable += timeit.timeit(stmt=lambda:
                                           h.add_list(lst), number=1)
        # toc = time.timer()
        # runtime_hashtable += toc - tic
        # test = h.get_table_entry_count()
        # print(str(test) + " " + str(n))  # for test
        # print(i)
    runtime_quicksort /= float(3)
    runtime_hashtable /= 3
    # print(runtime_quicksort)
    # print(runtime_hashtable)
    print(str(n) + '\t' + str(runtime_quicksort) + '\t' +
          str(runtime_hashtable))


def get_next_higher_prime_number(start):
    """ Calculates the next higher prime number
        start:  number to start for searching a prime number
    >>> get_next_higher_prime_number(98)
    101
    """
    if start > 1:
        isPrime = 0
        while not isPrime:
            # print(start)
            for i in range(2, start):
                if (start % i) == 0:
                    # print(i)
                    break
            else:
                isPrime = 1
                break
            start += 1
        # print("isPrime " + str(isPrime))
    return start

if __name__ == "__main__":
    for i in range(10, 17):
        n = 2**i
        # print(n)
        u = 2**i
        # p = 1073741827
        p = get_next_higher_prime_number(u)
        m = 2**10
        calculate_runtime(n, p, u, m)
