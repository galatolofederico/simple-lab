from simplelab.api.utils import existsfile

class Repository:
    def __init__(self, server, remote, path):
        self.server = server
        self.remote = remote
        self.path = path
        if self.exists():
            self.getstatus()
    
    def exists(self):
        return existsfile(self.server, self.path)
    
    def getstatus(self):
        name, _= self.server.cmd("cd "+self.path+" && basename $(git rev-parse --show-toplevel)")
        self.name = name.rstrip()
        branch, _ = self.server.cmd("cd "+self.path+" && git symbolic-ref --short -q HEAD")
        self.branch = branch.rstrip()
        commit, _ = self.server.cmd("cd "+self.path+" && git rev-parse HEAD")
        self.commit = commit.rstrip()
    
    def clone(self):
        execcmd(self.server, "git clone "+self.remote+" "+self.path)

    def build(self):
        pass
