import argparse

import numpy as np
from pandas.io import clipboard


def parse_args():
    parser = argparse.ArgumentParser(description="Generate random array")
    parser.add_argument("--seed", type=int, default=1234, help="random seed")
    parser.add_argument("--low", type=int, default=0, help="low value of array")
    parser.add_argument("--high", type=int, default=100, help="high value of array")
    parser.add_argument("--size", type=str, help="size of array", nargs="+")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    np.random.seed(args.seed)

    low = args.low
    high = args.high
    size = [int(x) for x in args.size]
    arr = np.random.randint(low, high, size=size, dtype=int)
    if len(arr.shape) == 1:
        arr = arr.reshape((1, -1))

    # convert arr to space separated string
    s = [' '.join(map(str, i.flatten())) for i in arr]
    s = '\n'.join(s)
    clipboard.copy(s)


if __name__ == "__main__":
    main()
