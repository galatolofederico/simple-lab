import os
import sys
import json

fifo = open("/tmp/simplelab.fifo", "w")
fifo.write(json.dumps({
    "repo": sys.argv[1],
    "cmd": sys.argv[2]
}))
fifo.close()