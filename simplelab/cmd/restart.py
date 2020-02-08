from simplelab.api.utils import execcmd, existsfile, execcmdpath
from simplelab.api.repository import Repository
import time

def restart(server):
    server.connect()
    if not server.connected: raise Exception("Not connected")
    if not server.getinstalled(): raise Exception("Not installed")

    if existsfile(server, "/tmp/simplelab_lock.pid"):
        execcmd(server, "pid=$(cat /tmp/simplelab_lock.pid); for p in $(pgrep -P $pid); do kill $p; done; kill $pid")
        execcmd(server, "rm -f /tmp/simplelab_lock.pid")
    
    time.sleep(1)
    try:
        cmd = "cd ~/simplelab && . ./env/bin/activate && nohup python -m simplelab.scheduler > /tmp/simplelab_scheduler.log &"
        print("[%s] executing: %s" %(server.name, cmd))
        server.cmd_timeout(cmd, 1)
    except:
        pass