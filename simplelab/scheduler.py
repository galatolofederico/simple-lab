import os
import sys
import json
import threading
import multiprocessing
import subprocess
import queue
import time

if not os.path.exists("/tmp/simplelab.fifo"):
    os.mkfifo("/tmp/simplelab.fifo")

def scheduler():
    global pool
    while True:
        fifo = open("/tmp/simplelab.fifo", "r")
        msg = json.loads(fifo.read())
        print("Received: %s" % (msg))
        #if msg["type"] == "cmd":
        cmd_queue.put(msg)

        fifo.close()

def runner():
    while True:
        msg = cmd_queue.get()
        if msg["type"] == "exit":
            break
        if msg["type"] == "cmd":
            folder = "./logs/%s" % (time.time())
            os.mkdir(folder)
            stdout = open(folder+"/stdout.log", "w")
            stderr = open(folder+"/stderr.log", "w")
            subprocess.run(msg["cmd"], shell=True, stdout=stdout, stderr=stderr)


cmd_queue = multiprocessing.Queue()
pool = [multiprocessing.Process(target=runner), multiprocessing.Process(target=runner),]

if __name__ == "__main__":
    scheduler_thread = threading.Thread(target=scheduler)
    
    scheduler_thread.start()

    for p in pool: p.start()
