import fractions
import math
import random
import cirq
import numpy as np
import sympy
from typing import Sequence, Iterable, Union

from ancillary import *


def factor_prime_pow(num):
    # Returns non-trivial factor of n if n is a prime power, else None
    for i in range(2, math.floor(math.log2(num)) + 1):
        c = math.pow(num, 1 / i)
            
        floor = math.floor(c)
        if floor**i == num:
            # print(f"a: {floor}")
            return floor

        ceil = math.ceil(c)
        if ceil**i == num:
            # print(f"b: {ceil}")
            return ceil

    # print("b")
    return None


def factor(num, finder, max_iter = 50):
    # returns a non-trivial factor of num

    # if num is even return 2
    if num % 2 == 0:
        return 2

    # if num is prime returns None
    if sympy.isprime(num):
        return None

    # if num is a prime power use factor_prime_pow function
    n = factor_prime_pow(num)
    if n != None:
        return n

    # if none of the above worked:
    for _ in range(max_iter):
        # select a random number
        rand = random.randint(2, num - 1)

        # probably they are co-prime, apply greatest common divisor
        n = math.gcd(rand, num)

        # if n == 1 they are coprime, else we have a factor
        if 1 < n < num:
            return num

        # we need to find the order of elements of the multiplicative group of integers modulo n
        theta = qof(rand, num)

         # if the order fails continue
        if theta is None:
            continue

        # if r is even continue
        if theta % 2 != 0:
            continue

        # compute the non-trivial factor
        y = rand**(theta // 2) % num

        assert 1 < y < num

        n = math.gcd(y - 1, num)

        if 1 < n < num:
            return n

        print(f"Failed")
        return None


def qof(x, n):
    # computes smallest positive r such that x**r mod n == 1

    # check x is a valid element of the multiplicative group modulo n
    if x < 2 or n <= x or math.gcd(x, n) > 1:
        raise ValueError(f'Invalid x={x} for modulus n={n}.')

    # setup
    c = make_order_finding_circuit(x, n)

    # simulates sampling from the given circuit
    m = cirq.sample(c)

    # Return the processed measurement result.
    return process_measurement(m, x, n)


# Number to factor
n = 15

# Attempt to find a factor
p = factor(n, qof)
if p != None:
    q = n // p

    print("Factoring n = pq =", n)
    print("p =", p)
    print("q =", q)

else:
    print(f"{n} is prime or something went wrong")