import yaml
import sys
import os

servers = None
def loadservers():
    global servers
    try:
        with open(os.path.expanduser("~/.config/lab.servers.yml")) as f:
            servers = yaml.load(f, Loader=yaml.FullLoader)
    except:
        print("File ~/.config/lab.servers.yml not found!")
        sys.exit(1)

def main():
    loadservers()
    print("a", servers)