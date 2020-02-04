from simplelab.api.utils import loadservers, getserver, parsearguments, initservers
from simplelab.cmd.status import status

def main():
    servers = initservers(loadservers())
    args = parsearguments(servers)
    if args.cmd == "run":
        run(args.server, args.args)
    elif args.cmd == "status":
        status(servers)
    elif args.cmd == "install":
        install(args.server)
    elif args.cmd == "shared":
        shared(args.server, args.args)