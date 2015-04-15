import encoder
import xqluser
from client import Client
from xqluser import XqlUser
import socket
import select


def new_connection(s):
    connection, client_address = s.accept()
    connection.setblocking(0)
    inputs.append(connection)
    outputs.append(connection)
    clients[client_address] = Client(client_address, connection)
    print "new slave server from ", client_address


def close_connection(s):
    client = clients[s.getpeername()]
    print "closing", client.peername
    if s in outputs:
        outputs.remove(s)
    inputs.remove(s)
    s.close()


def get_msg_from_client(s):
    client = clients[s.getpeername()]
    try:
        data = s.recv(1024)
    except:
        data = ''
    if data:
        print "receive ", data, "from ", client.peername
        clients[client.peername].handle_msg(data)
    else:
        close_connection(s)


def mainloop():
    readable, writable, exceptional = select.select(inputs, outputs, inputs, timeout)
    for s in readable:
        if s is server:
            new_connection(s)
        else:
            get_msg_from_client(s)
    for s in writable:
        clients[s.getpeername()].send_msg()
    for s in exceptional:
        print "exception condition on ", s.getpeername()
        close_connection(s)


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_address = ('', 9998)
    server.bind(server_address)
    server.listen(100)
    return server


server = start_server()
clients = {}
inputs = [server]
outputs = []
timeout = 2
while inputs:
    mainloop()
