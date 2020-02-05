from simplelab.api.utils import existsfile, execcmd, execcmdpath

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
    
    def clone(self, secrets):
        uri = self.remote
        if secrets is not None:
            print("[%s] creating /tmp/gitaskpass.sh file" % (self.server.name))
            self.server.cmd("echo exec echo "+secrets["password"]+" > /tmp/gitaskpass.sh")
            self.server.cmd("chmod +x /tmp/gitaskpass.sh")
            proto = uri.split("//")[0]
            loc = uri.split("//")[1]
            uri = proto+"//"+secrets["username"]+"@"+loc
            execcmd(self.server, "GIT_ASKPASS=/tmp/gitaskpass.sh git clone "+uri+" "+self.path)
            print("[%s] deleting /tmp/gitaskpass.sh file" % (self.server.name))
            self.server.cmd("rm /tmp/gitaskpass.sh")
        else:
            execcmd(self.server, "git clone "+self.remote+" "+self.path)
        
        if self.exists():
            print("[%s] Correctly cloned in the remote server" % (self.server.name))
        else:
            raise Exception("There was an error cloning the repository in the remote server %s" % (self.server.name))


    def build(self, labyaml):
        if "build" in labyaml:
            for asset in labyaml["build"]:
                if not existsfile(self.server, self.path+"/"+asset):
                    for cmd in labyaml["build"][asset]:
                        execcmdpath(self.server, cmd, self.path)
        
        if "shares" in labyaml:
            basedir = "~/simplelab/shares/"+self.name
            if not existsfile(self.server, basedir):
                execcmd(self.server, "mkdir "+basedir)
            if "directories" in labyaml["shares"]:
                for directory in labyaml["shares"]["directories"]:
                    if not existsfile(self.server, basedir+"/"+directory):
                        execcmd(self.server, "mkdir "+basedir+"/"+directory)



    def checkoutbranch(self, branch):
        execcmdpath(self.server, "git checkout %s || git checkout -b %s" % (branch, branch), self.path)
        self.getstatus()
    
    def checkoutcommit(self, commit):
        execcmdpath(self.server, "git reset --hard %s" % (commit), self.path)
        self.getstatus()

    def pull(self):
        execcmdpath(self.server, "git pull origin %s" % (self.branch), self.path)