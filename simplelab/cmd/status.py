from prettytable import PrettyTable

def status(servers):
    table = PrettyTable()
    table.field_names = ["Server", "Default", "Status", "Running", "Queued", "Slots"]
    for server in servers:
        server.connect()
        table.add_row([server.name, server.default, server.getstatus(), server.getrunning(), server.getqueued(), server.getslots()])
        
    print(table)