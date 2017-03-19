#!/usr/bin/env python3
import math


def calculate_runtime(n):
    if n <= 1:
        return 1
    else:
        return 4*calculate_runtime(math.ceil(n/2)) + n**2

if __name__ == "__main__":
    n = 2**20
    c1 = 1
    c2 = 3
    for i in range(1, n+1):
        f1 = c1*i**2*math.log(i)
        f2 = calculate_runtime(i)
        f3 = c2*i**2*math.log(i)
        if i % 10000 == 0:
            print(str(i) + "\t" + str(f1) + "\t" + str(f2) + "\t" + str(f3))
