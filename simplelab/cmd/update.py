
def update(server):
    server.connect()
    if not server.connected: raise Exception("Not connected")
    if not server.getinstalled(): raise Exception("Not installed")

    server.cmd("cd simplelab && git pull origin master")

    print("simplelab updated on %s" % (server.name))