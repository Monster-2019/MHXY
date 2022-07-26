import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--shutdown', '-s', action='store_true', default=False)
parser.add_argument('--time', '-t', type=str)

args = parser.parse_args()
print(args)