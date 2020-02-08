from simplelab.api.utils import listdir
from simplelab.api.server.localserver import LocalServer
from simplelab.api.repository import Repository


def logs(server, args):
    server.connect()
    if not server.connected: raise Exception("Not connected")
    if not server.getinstalled(): raise Exception("Not installed")
    if not server.getready(): raise Exception("Not ready")
    
    local = LocalServer()
    local.connect()

    stdout, _ = local.cmd("git remote get-url origin")
    remote = stdout.rstrip()
    stdout, _ = local.cmd("pwd")
    path = stdout.rstrip()

    localrepo = Repository(local, remote, path)
    
    print(listdir(server, "~/simplelab/logs/"+localrepo.name))
