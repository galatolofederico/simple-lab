from simplelab.api.server.server import Server

class LocalServer(Server):
    def __init__(self):
        super(LocalServer, self).__init__(name="localhost", default=False)
        self.connected = False

    def connect(self):
        self.connected = True