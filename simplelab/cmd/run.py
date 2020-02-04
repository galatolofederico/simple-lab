from simplelab.api.utils import execcmd
from simplelab.api.server.localserver import LocalServer
from simplelab.api.repository import Repository


def run(server, args):
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

    stdout, _ = local.cmd("git status -s")
    if len(stdout) > 0: raise Exception("Unstaged changes in the repository, Please commit or stash them.")
    stdout, _ = local.cmd("git diff origin/"+localrepo.branch+"..HEAD")
    if len(stdout) > 0: raise Exception("Unpushed commits in the repository, Please push them.")


    if not remoterepo.exists():
        remoterepo.clone()
        remoterepo.build()
    