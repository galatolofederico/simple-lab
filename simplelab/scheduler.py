import os
import sys
import json
import threading
import multiprocessing
import subprocess
import queue
import time

if not os.path.exists("/tmp/simplelab_cmd.fifo"):
    os.mkfifo("/tmp/simplelab_cmd.fifo")
if not os.path.exists("/tmp/simplelab_ans.fifo"):
    os.mkfifo("/tmp/simplelab_ans.fifo")

def ans(s):
    ans_fifo = open("/tmp/simplelab_ans.fifo", "w")
    ans_fifo.write(str(s))
    ans_fifo.close()


def scheduler():
    global pool
    global slots
    while True:
        pool = list(filter(lambda p: p.is_alive(), pool))
        fifo = open("/tmp/simplelab_cmd.fifo", "r")
        msg = json.loads(fifo.read())
        print("Received: %s" % (msg))
        if msg["type"] == "get":
            if msg["res"] == "processes":
                ans(len(pool))
            if msg["res"] == "queued":
                ans(cmd_queue.qsize())
            if msg["res"] == "slots":
                ans(slots)
            
        elif msg["type"] == "set":
            if msg["res"] == "slots":
                val = int(msg["val"])
                if val - len(pool) > 0:
                    for _ in range(0, val-len(pool)):
                        p = multiprocessing.Process(target=runner)
                        p.start()
                        pool.append(p)
                elif len(pool) - val > 0:
                    for _ in range(0, len(pool)-val): cmd_queue.put(dict(type="exit"))
                slots = val
        else:
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
pool = [multiprocessing.Process(target=runner)]
slots = 1

if __name__ == "__main__":
    scheduler_thread = threading.Thread(target=scheduler)
    
    for p in pool: p.start()
    
    scheduler_thread.start()
