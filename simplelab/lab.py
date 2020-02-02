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
        


def parsearguments():
    help_str = """lab [server] action
if [server] is omitted the default one is used
action can be:

* run <cmd>: Start experiment on [server] with command <cmd>
* status: Check the status of all the servers
* install: Install simplelab to server [server]
* shared list: List all the experiment shared assets
* shared clear <name>: Clear the content of shared assets <name>
"""
    server, shift = getserver(sys.argv[1])
    args = sys.argv[1:]
    if shift: args = args[1:]
    Args = collections.namedtuple('Args', ['server', 'cmd', 'args'])

    return Args(server, args[0], args[1:])


def main():
    loadservers()
    args = parsearguments()
    print(args)