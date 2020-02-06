import os
import sys
import json
import threading
import multiprocessing
import queue

if not os.path.exists("/tmp/simplelab.fifo"):
    os.mkfifo("/tmp/simplelab.fifo")

def scheduler():
    global pool
    while True:
        fifo = open("/tmp/simplelab.fifo", "r")
        msg = json.loads(fifo.read())
        #if msg["type"] == "cmd":
        cmd_queue.put(msg)

        fifo.close()

def runner():
    while True:
        msg = cmd_queue.get()
        print("runner", msg)
        if msg["type"] == "exit":
            break
        import time
        time.sleep(4)

cmd_queue = multiprocessing.Queue()
pool = [multiprocessing.Process(target=runner), multiprocessing.Process(target=runner),]

if __name__ == "__main__":
    scheduler_thread = threading.Thread(target=scheduler)
    
    scheduler_thread.start()

    for p in pool: p.start()
