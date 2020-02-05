from simplelab.api.utils import execcmd
from simplelab.api.server.localserver import LocalServer
from simplelab.api.repository import Repository


def remove(server):
    server.connect()
    if not server.connected: raise Exception("Not connected")
    if not server.getinstalled(): raise Exception("Not installed")

    local = LocalServer()
    local.connect()

    stdout, _ = local.cmd("git remote get-url origin")
    remote = stdout.rstrip()
    stdout, _ = local.cmd("pwd")
    path = stdout.rstrip()
    

    localrepo = Repository(local, remote, path)
    remoterepo = Repository(server, remote, "~/simplelab/repositories/"+localrepo.name)

    if not remoterepo.exists(): raise Exception("Remote repository do not exists")
    
    execcmd(remoterepo.server, "rm -rf %s" % (remoterepo.path))

    if not remoterepo.exists():
        print("Remote repository successfully deleted")
    