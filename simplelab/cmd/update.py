from simplelab.api.utils import checkcmd, execcmd, execcmdpath
from simplelab.cmd.restart import restart

def update(server):
    server.connect()
    if not server.connected: raise Exception("Not connected")
    if not server.getinstalled(): raise Exception("Not installed")

    print("updating simplelab on %s" % (server.name))

    checkcmd(server, "git")
    checkcmd(server, "virtualenv")

    execcmdpath(server, ". ./env/bin/activate && pip uninstall simplelab -y", "~/simplelab")
    execcmdpath(server, "git pull origin master", "~/simplelab")
    execcmdpath(server, ". ./env/bin/activate && python setup.py install", "~/simplelab")
    
    restart(server)

    print("simplelab updated on %s" % (server.name))