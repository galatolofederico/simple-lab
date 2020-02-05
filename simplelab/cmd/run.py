from simplelab.api.utils import execcmd
from simplelab.api.server.localserver import LocalServer
from simplelab.api.repository import Repository
import yaml
import os

def loadyaml(fname):
    if os.path.isfile(fname):
        f = open(fname)
        return yaml.load(f, Loader=yaml.FullLoader)
    else:
        return None


def run(server, args):
    labyml = loadyaml("./lab.yml")
    secrets = loadyaml("./secrets.yml")
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
        remoterepo.clone(secrets)
    
    remoterepo.build(labyml)

    if remoterepo.branch != localrepo.branch:
        remoterepo.checkoutbranch(localrepo.branch)
    
    remoterepo.pull()
    if remoterepo.commit != localrepo.commit:
        remoterepo.checkoutcommit(localrepo.commit)

    mods = []
    if "run" in labyml:
        mods.extend(labyml["run"])

    mods.extend(remoterepo.getshares(labyml))
    
    cmd = " ".join(args)
    for mod in mods:
        assert len(list(mod.keys())) == 1
        a = list(mod.keys())[0]
        v = mod[a]
        if a == "prepend":
            cmd = v+" "+cmd
        if a == "append":
            cmd = cmd+" "+v
    
    #TODO: schedule cmd
    print(cmd)
