import subprocess
from simplelab.api.server.server import Server

class LocalServer(Server):
    def __init__(self):
        super(LocalServer, self).__init__(name="localhost", default=False)
        self.connected = False

    def connect(self):
        self.connected = True
    
    def cmd(self, cmd):
        proc = subprocess.Popen(cmd,
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            shell=True
        )
        stdout, stderr = proc.communicate()
        
        return stdout.decode("utf-8"), stderr.decode("utf-8")