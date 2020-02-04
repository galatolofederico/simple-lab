from simplelab.api.utils import checkcmd, execcmd

def update(server):
    server.connect()
    if not server.connected: raise Exception("Not connected")
    if not server.getinstalled(): raise Exception("Not installed")

    print("updating simplelab on %s" % (server.name))

    checkcmd(server, "git")
    checkcmd(server, "virtualenv")

    execcmd(server, "cd ~/simplelab && . ./env/bin/activate && pip uninstall simplelab -y")
    execcmd(server, "cd ~/simplelab && git pull origin master")
    execcmd(server, "cd ~/simplelab && . ./env/bin/activate && python setup.py install")
    

    print("simplelab updated on %s" % (server.name))