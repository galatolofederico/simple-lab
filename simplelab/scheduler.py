import os
import sys
import json
import threading

if not os.path.exists("/tmp/simplelab.fifo"):
    os.mkfifo("/tmp/simplelab.fifo")

msg_queue = threading.Queue()

def recv():
    fifo = open("/tmp/simplelab.fifo", "r")
    for msg in fifo:
        msg_queue.put(json.loads(msg))

def scheduler():
    msg = msg_queue.get()
    
    
