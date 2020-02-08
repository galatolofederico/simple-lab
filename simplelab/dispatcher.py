import os
import argparse
import json
import sys
import threading

parser = argparse.ArgumentParser()

parser.add_argument('--type')
parser.add_argument('--cmd')
parser.add_argument('--res')
parser.add_argument('--val')


args = parser.parse_args()    

fifo = open("/tmp/simplelab_cmd.fifo", "w")
fifo.write(json.dumps(vars(args)))
fifo.close()

if args.type == "get":
    ans_fifo = open("/tmp/simplelab_ans.fifo", "r")
    print(ans_fifo.read())
    ans_fifo.close()