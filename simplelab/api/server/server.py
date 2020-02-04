import paramiko
from simplelab.api.utils import existsfile

class Server:
    def __init__(self, **kwargs):
        self.args = kwargs
        self.name = kwargs["name"]
        self.default = kwargs["default"] if "default" in kwargs else False
        
    def getinstalled(self):
        if not self.connected: return False
        return existsfile(self, "~/simplelab")

    def getrunning(self):
        if not self.connected: return None
        return 0
    
    def getqueued(self):
        if not self.connected: return None
        return 0

    def getstatus(self):
        status = "Offline"
        if self.connected: status = "Online (lab not installed)"
        if self.getinstalled(): status = "Ready"
        return status