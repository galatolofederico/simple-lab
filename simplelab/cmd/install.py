from simplelab.api.utils import checkcmd, execcmd, execcmdpath
from simplelab.cmd.restart import restart

def install(server):
    server.connect()
    if not server.connected: raise Exception("Not connected")
    if server.getinstalled(): raise Exception("Already installed")

    print("installing simplelab on %s" % (server.name))

    checkcmd(server, "git")
    checkcmd(server, "virtualenv")

    execcmd(server, "git clone https://github.com/galatolofederico/simple-lab.git ~/simplelab")
    execcmdpath(server, "virtualenv env", "~/simplelab")
    execcmdpath(server, ". ./env/bin/activate && python setup.py install", "~/simplelab")    

    restart(server)

    print("simplelab installed on %s" % (server.name))