#!/usr/bin/python3

import sys


def compute_ed_recursively(x, y):
    """ Compute edit distance from x to y recursively.

    >>> compute_ed_recursively("", "")
    0
    >>> compute_ed_recursively("donald", "ronaldo")
    2
    """
    n = len(x)
    m = len(y)
    if n == 0:
        return m
    if m == 0:
        return n
    # Insert case.
    ed1 = compute_ed_recursively(x, y[0:-1]) + 1
    # Delete case.
    ed2 = compute_ed_recursively(x[0:-1], y) + 1
    # Replace case.
    ed3 = compute_ed_recursively(x[0:-1], y[0:-1])
    # If last characters do not match, add replace costs.
    if x[-1] != y[-1]:
        ed3 += 1
    return min(ed1, ed2, ed3)


def compute_ed_via_table(x, y):
    """ Compute edit distance via dynamic programming table.

    >>> compute_ed_via_table("", "")
    0
    >>> compute_ed_via_table("test", "")
    4
    >>> compute_ed_via_table("", "test")
    4
    >>> compute_ed_via_table("donald", "ronaldo")
    2
    """
    # Initalitze table
    table = [[0]*(len(y) + 1) for i in range(len(x) + 1)]
    for i in range(len(x) + 1):
        for j in range(len(y) + 1):
            if i == 0:
                table[i][j] = j
            elif j == 0:
                table[i][j] = i
            else:
                table[i][j] = 0
    # print(table)
    # Calcs costs
    for i in range(1, len(x)+1):
        for j in range(1, len(y)+1):  # search predecessor with lowest costs
            delCosts = table[i][j-1]
            insCosts = table[i-1][j]
            replCosts = table[i-1][j-1]
            table[i][j] = min(delCosts, min(insCosts, replCosts))
            if x[i-1] != y[j-1]:  # Cost increase necessary
                table[i][j] += 1
    # print(table)
    return table[i][j]


if __name__ == "__main__":
    # Read in two strings from command line.
    nr_args = len(sys.argv)
    if not nr_args == 3:
        raise Exception("script excepts two input strings")
    x = sys.argv[1]
    y = sys.argv[2]
    print("x = %s" % (x))
    print("y = %s" % (y))
    ed = compute_ed_recursively(x, y)
    print("Edit distance (x -> y): %i" % (ed))
