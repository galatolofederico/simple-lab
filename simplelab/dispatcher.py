import os
import argparse
import json

parser = argparse.ArgumentParser()

parser.add_argument('--type')
parser.add_argument('--repo')
parser.add_argument('--cmd')

args = parser.parse_args()

fifo = open("/tmp/simplelab.fifo", "w")
fifo.write(json.dumps(vars(args)))
fifo.close()