import paramiko
from simplelab.api.utils import existsfile, execcmdpath

class Server:
    def __init__(self, **kwargs):
        self.args = kwargs
        self.name = kwargs["name"]
        self.default = kwargs["default"] if "default" in kwargs else False
        
    def getinstalled(self):
        if not self.connected: return False
        return existsfile(self, "~/simplelab")

    def getrunning(self):
        if not self.getready(): return None
        if not self.connected: return None
        ans, _ = execcmdpath(self, ". ./env/bin/activate && python -m simplelab.dispatcher --type get --res running", "~/simplelab")
        return 0
    
    def getqueued(self):
        if not self.connected: return None
        if not self.getready(): return None
        ans, _ = execcmdpath(self, ". ./env/bin/activate && python -m simplelab.dispatcher --type get --res queued", "~/simplelab")
    
    def getready(self):
        if not self.connected: return None
        return existsfile(self, "/tmp/simplelab_lock.pid")

    def getstatus(self):
        status = "Offline"
        if self.connected: status = "Online (lab not installed)"
        if self.getinstalled(): status = "Installed"
        if self.getready(): status = "Ready"
        return status