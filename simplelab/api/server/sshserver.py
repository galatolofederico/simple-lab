import paramiko
from simplelab.api.server.server import Server

class SSHServer(Server):
    def __init__(self, **kwargs):
        super(SSHServer, self).__init__(**kwargs)
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
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
    
    def cmd(self, cmd):
        if not self.connected: raise Exception("Not connected")
        stdin, stdout, stderr = self.client.exec_command(cmd)
        return stdout.read().decode("utf-8"), stderr.read().decode("utf-8")


    def cmd_timeout(self, cmd, timeout):
        if not self.connected: raise Exception("Not connected")
        stdin, stdout, stderr = self.client.exec_command(cmd, timeout=timeout)
        return stdout.read().decode("utf-8"), stderr.read().decode("utf-8")
