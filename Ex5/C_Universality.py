#!/usr/bin/env python
import random as rnd


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


def mean_bucket_size(S, h):
    BucketIndex = []
    for i in range(len(S)):
        # Gets the bucket for each key in S
        BucketIndex.append(h.apply(S[i]))
    # Make Bucket number unique, equals used buckets
    UniqueBucketIndex = set(BucketIndex)
    # Clacs the nbr_of_bucket div nbr_of_used_buckets
    # Unused buckets do not contain any elements
    # => they have to be ignored
    # print h.hashtable
    # print len(S)/len(UniqueBucketIndex)
    return len(S)/len(UniqueBucketIndex)


def estimate_c_for_single_set(S, h):
    c_min = float('inf')
    for i in range(1000):  # should be 1000
        h.set_random_parameters()
        # c = (mean_bucket_size(S, h) - 1)/len(S)*h.m
        c = (float)(mean_bucket_size(S, h) - 1)/len(S)*h.m
        # if c != 0:
        #     print c, c_min, len(S), h.m
        if c_min > c:
            c_min = c
    # print c_min
    return c_min


def estimate_c_for_multiple_set(n, k, h):
    c_min = float('inf')
    c_max = 0
    c_sum = 0
    for i in range(n):
        c = estimate_c_for_single_set(create_random_universe_subset(k, h.u), h)
        c_sum += c
        if c < c_min:
            c_min = c
        if c > c_max:
            c_max = c
    # print c, c_sum, c_min, c_max
    return c_sum/n, c_min, c_max


def create_random_universe_subset(k, u):
    n = set([])
    while len(n) <= k-1:
        n.add(rnd.randrange(0, u, 1))
        n = set(n)
    n = list(n)
    # print n
    return n


if __name__ == "__main__":
    u = 100  # 100
    m = 100  # 100
    p1 = 101  # 101
    n = 1000  # 1000
    k = 20  # 20
    h1 = HashFunction(p1, u, m)
    print("* Case 1 *")
    print("Universe size u=" + str(u) + " Hashtable size m=" + str(m) + " p=" +
          str(p1) + " number of key sets n=" + str(n) + " key set size k=" +
          str(k))
    c_avg, c_min, c_max = estimate_c_for_multiple_set(n, k, h1)
    print("C_Average: " + str(c_avg) + " C_min: " + str(c_min) + " C_max: " +
          str(c_max))
    p2 = 10
    h2 = HashFunction(p2, u, m)
    print("\n")
    print("* Case 2 *")
    print("Universe size u=" + str(u) + " Hashtable size m=" + str(m) + " p=" +
          str(p2) + " number of key sets n=" + str(n) + " key set size k=" +
          str(k))
    c_avg, c_min, c_max = estimate_c_for_multiple_set(n, k, h2)
    print("C_Average: " + str(c_avg) + " C_min: " + str(c_min) + " C_max: " +
          str(c_max))
