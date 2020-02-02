import yaml
import sys
import os
import collections

servers = None
def loadservers():
    global servers
    try:
        with open(os.path.expanduser("~/.config/lab.servers.yml")) as f:
            servers = yaml.load(f, Loader=yaml.FullLoader)
    except:
        print("File ~/.config/lab.servers.yml not found!")
        sys.exit(1)


def getserver(name):
    default = servers[0]
    for server in servers:
        if "default" in server and server["default"]:
            default = server
        if server["name"] == name:
            return server, True
    return default, False
        
def print_help():
    print("""lab [server] action
if [server] is omitted the default one is used
action can be:

* run <cmd>: Start experiment on [server] with command <cmd>
* status: Check the status of all the servers
* install: Install simplelab to server [server]
* shared list: List all the experiment shared assets
* shared clear <name>: Clear the content of shared assets <name>
""")
    sys.exit(1)


def parsearguments():
    try:
        server, shift = getserver(sys.argv[1])
        args = sys.argv[1:]
        if shift: args = args[1:]
        Args = collections.namedtuple('Args', ['server', 'cmd', 'args'])
    except:
        print_help()
    if args[0] not in ["run", "status", "install", "shared"]:
        print_help()
    
    return Args(server, args[0], args[1:])


def main():
    loadservers()
    args = parsearguments()
    if args.cmd == "run":
        run(args.server, args.args)
    elif args.cmd == "status":
        status()
    elif args.cmd == "install":
        install(args.server)
    elif args.cmd == "shared":
        shared(args.server, args.args)