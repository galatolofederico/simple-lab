import yaml
import sys
import os
import collections

from simplelab.api.server.sshserver import SSHServer
from simplelab.api.server.localserver import LocalServer

def loadservers():
    fname = os.path.expanduser("~/.config/lab.servers.yml")
    if os.path.isfile(fname):
        f = open(fname)
        return yaml.load(f, Loader=yaml.FullLoader)
    else:
        return []

def getserver(name, servers):
    default = servers[0]
    for server in servers:
        if server.default:
            default = server
        if server.name == name:
            return server, True
    return default, False
        
def print_help():
    print("""lab [server] action
if [server] is omitted the default one is used
action can be:

* run <cmd>: Start experiment on [server] with command <cmd>
* status: Check the status of all the servers
* install: Install simplelab to [server]
* update: Update simplelab on [server]
* shared list: List all the experiment shared assets
* shared clear <name>: Clear the content of shared assets <name>
""")
    sys.exit(1)


def parsearguments(servers):
    if len(sys.argv) <= 1:
        print_help()
    server, shift = getserver(sys.argv[1], servers)
    args = sys.argv[1:]
    if shift: args = args[1:]
    Args = collections.namedtuple('Args', ['server', 'cmd', 'args'])
    if args[0] not in ["run", "status", "install", "shared", "update"]:
        print_help()
    
    return Args(server, args[0], args[1:])



def initservers(servers):
    ret = [LocalServer()]
    for server in servers:
        if server["login_method"] == "ssh_password":
            ret.append(SSHServer(**server))
    
    return ret



def checkcmd(server, prog):
    print("[%s] checking for: %s" % (server.name, prog))
    _, stderr = server.cmd(prog)
    if len(stderr) > 0:
        raise Exception("You need to install %s on %s" % (prog, server.name))

def execcmd(server, cmd):
    print("[%s] executing: %s" % (server.name, cmd))
    _, stderr = server.cmd(cmd)