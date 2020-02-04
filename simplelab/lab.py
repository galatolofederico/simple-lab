from simplelab.api.utils import loadservers, parsearguments, initservers

from simplelab.cmd.status import status
from simplelab.cmd.install import install
from simplelab.cmd.update import update


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