from simplelab.api.utils import loadservers, parsearguments

from simplelab.cmd.run import run
from simplelab.cmd.status import status
from simplelab.cmd.install import install
from simplelab.cmd.update import update
from simplelab.cmd.remove import remove

from simplelab.api.server.sshserver import SSHServer
from simplelab.api.server.localserver import LocalServer

def initservers(servers):
    ret = [LocalServer()]
    for server in servers:
        if server["login_method"] == "ssh_password":
            ret.append(SSHServer(**server))
    
    return ret

def main():
    servers = initservers(loadservers())
    args = parsearguments(servers)
    if args.cmd == "run":
        run(args.server, args.args)
    elif args.cmd == "status":
        status(servers)
    elif args.cmd == "install":
        install(args.server)
    elif args.cmd == "update":
        update(args.server)
    elif args.cmd == "shared":
        shared(args.server, args.args)
    elif args.cmd == "remove":
        remove(args.server)