from simplelab.api.utils import checkcmd, execcmd

def install(server):
    server.connect()
    if not server.connected: raise Exception("Not connected")
    if server.getinstalled(): raise Exception("Already installed")

    print("installing simplelab on %s" % (server.name))

    checkcmd(server, "git")
    checkcmd(server, "virtualenv")

    execcmd(server, "git clone https://github.com/galatolofederico/simple-lab.git ~/simplelab")
    execcmd(server, "cd ~/simplelab && virtualenv env")
    execcmd(server, "cd ~/simplelab && . ./env/bin/activate && python setup.py install")    

    print("simplelab installed on %s" % (server.name))