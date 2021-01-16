#!/home/fernando/Anaconda/envs/dev/bin/python

import get

block = int(get.inputnum("Height: "))

if 1 <= block <= 8:
    for i in range(1, block + 1):
        print(" " * (block - i) + "#" * (i), end="")
        print("  ", end="")
        print("#" * (i))
