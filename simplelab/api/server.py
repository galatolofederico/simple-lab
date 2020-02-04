import paramiko

class Server:
    def __init__(self, **kwargs):
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.args = kwargs
        self.name = kwargs["name"]
        self.default = kwargs["default"] if "default" in kwargs else False
        self.connected = False

    def connect(self):
        if self.connected: return
        if self.args["login_method"] == "ssh_password":
            try:
                self.client.connect(self.args["ip"], 
                            username=self.args["username"],
                            password=self.args["password"],
                            timeout=2, banner_timeout=2,
                            auth_timeout=2)
                self.connected = True
            except:
                pass
    
    def getinstalled(self):
        return False

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