#!/usr/bin/python3
# Bart Massey

# Render an ASCII image from a template, constructed such
# that the digits in the resulting image form a large prime
# number.

# This code is licensed under the "MIT license".  See
# the file `LICENSE` in this distribution for license terms.

import random
import sys

# Miller-Rabin test below is recursive, and this number is
# going to be big. Should probably re-implement Miller-Rabin
# iteratively.
sys.setrecursionlimit(10000)

if len(sys.argv) > 1:
    picfile = open(sys.argv[1], "r")
else:
    picfile = sys.stdin
pic = picfile.read()

# Miller-Rabin probabilistic primality test.
# Code based on a 1999 Nickle implementation by me.
def is_composite(n, d):
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    
    def witness_exp(b, e, m):
        if e == 0:
            return (0, 1)
        if e == 1:
            return (b % m, 0)
        p, w = witness_exp(b, e // 2, m)
        if w != 0:
            return (p, w)
        t = (p ** 2) % m
        if t == 1 and p != 1 and p != m - 1:
            return (t, p)
        if e % 2 == 0:
            return (t, w)
        return ((t * b) % m, w)

    def witness(a, n):
        p, w = witness_exp(a, n - 1, n)
        if w != 0:
            return True
        if p != 1:
            return True
        return False

    for p in primes:
        if n % p == 0:
            return True
    for _ in range(d):
        a = 1 + random.randrange(n - 1)
        if witness(a, n):
            return True
    return False

# Repeatedly fill in the . characters in the template with
# random digits and see if the resulting number is prime.
while True:
    tn = ""
    for c in pic:
        if c == '.':
            tn += chr(ord('0') + random.randrange(10))
            continue
        if c.isnumeric():
            tn += c
    if not is_composite(int(tn), 40):
        break

# Substitute the . characters in the original pic template
# to produce a prime-pic.
ti = 0
tl = list(pic)
for i, c in enumerate(tl):
    if c.isnumeric():
        assert tn[ti] == c
        ti += 1
        continue
    if c == '.':
        tl[i] = tn[ti]
        ti += 1

# Render the pic.
print(''.join(tl))
