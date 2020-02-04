from prettytable import PrettyTable

def status(servers):
    table = PrettyTable()
    table.field_names = ["Server", "Status", "Running", "Queued"]
    for server in servers:
        server.connect()
        table.add_row([server.name, server.getstatus(), server.getrunning(), server.getqueued()])
        
    print(table)