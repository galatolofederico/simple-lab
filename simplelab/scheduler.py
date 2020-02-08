import os
import sys
import json
import threading
import multiprocessing
import subprocess
import queue
import time
import signal

def signals_handler(signum, frame):
    if os.path.exists("/tmp/simplelab_lock.pid"):
        os.remove("/tmp/simplelab_lock.pid")
    sys.exit()

def ans(s):
    ans_fifo = open("/tmp/simplelab_ans.fifo", "w")
    ans_fifo.write(str(s))
    ans_fifo.close()


def scheduler():
    global pool
    global slots
    global running
    while True:
        pool = list(filter(lambda p: p.is_alive(), pool))
        fifo = open("/tmp/simplelab_cmd.fifo", "r")
        msg = json.loads(fifo.read())
        print("Received: %s" % (msg))
        if msg["type"] == "get":
            if msg["res"] == "processes":
                ans(len(pool))
            elif msg["res"] == "queued":
                ans(cmd_queue.qsize())
            elif msg["res"] == "slots":
                ans(slots)
            elif msg["res"] == "running":
                ans(running)
            
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


def counter():
    global running
    while True:
        running += count_queue.get()

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
            count_queue.put(1)
            subprocess.run(msg["cmd"], shell=True, stdout=stdout, stderr=stderr)
            count_queue.put(-1)

if __name__ == "__main__":

    if os.path.exists("/tmp/simplelab_lock.pid"):
        print("Already Running")
        sys.exit()
    else:
        pidfile = open("/tmp/simplelab_lock.pid", "w")
        pidfile.write(str(os.getpid()))
        pidfile.close()


    signal.signal(signal.SIGINT, signals_handler)
    signal.signal(signal.SIGTERM, signals_handler)

    if not os.path.exists("/tmp/simplelab_cmd.fifo"):
        os.mkfifo("/tmp/simplelab_cmd.fifo")
    if not os.path.exists("/tmp/simplelab_ans.fifo"):
        os.mkfifo("/tmp/simplelab_ans.fifo")

    cmd_queue = multiprocessing.Queue()
    count_queue = multiprocessing.Queue()

    pool = [multiprocessing.Process(target=runner)]
    slots = 1
    running = 0

    if __name__ == "__main__":
        scheduler_thread = threading.Thread(target=scheduler)
        counter_thread = threading.Thread(target=counter)
        
        for p in pool: p.start()
        
        scheduler_thread.start()
        counter_thread.start()
