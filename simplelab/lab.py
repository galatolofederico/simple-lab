from simplelab.api.utils import loadservers, getserver, parsearguments
from simplelab.api.server import Server
from simplelab.cmd.status import status

servers = None

def main():
    servers = [Server(**server) for server in loadservers()]
    args = parsearguments(servers)
    if args.cmd == "run":
        run(args.server, args.args)
    elif args.cmd == "status":
        status(servers)
    elif args.cmd == "install":
        install(args.server)
    elif args.cmd == "shared":
        shared(args.server, args.args)