
def install(server):
    server.connect()
    if not server.connected: raise Exception("Not connected")
    if server.getinstalled(): raise Exception("Already installed")

    server.cmd("git clone https://github.com/galatolofederico/simple-lab.git ~/simplelab")
    server.cmd("mkdir ~/simplelab/repositories")

    print("simplelab installed on %s" % (server.name))