from client import Client
import socket
import select


class MainServer():
    def new_connection(self, s):
        connection, client_address = s.accept()
        connection.setblocking(0)
        self.inputs.append(connection)
        self.outputs.append(connection)
        self.clients[client_address] = Client(client_address, connection)
        print "new slave server from ", client_address

    def close_connection(self, s):
        client = self.clients[s.getpeername()]
        if s in self.outputs:
            self.outputs.remove(s)
        self.inputs.remove(s)
        s.close()
        print "closing", client.peername

    def get_msg_from_client(self, s):
        client = self.clients[s.getpeername()]
        try:
            data = s.recv(1024)
        except:
            data = ''
        if data:
            print "receive ", data, "from ", client.peername
            self.clients[client.peername].handle_msg(self, data)
        else:
            self.close_connection(s)

    def mainloop(self):
        readable, writable, exceptional = select.select(self.inputs, self.outputs, self.inputs, self.timeout)
        for s in readable:
            if s is self.server:
                self.new_connection(s)
            else:
                self.get_msg_from_client(s)
        for s in writable:
            self.clients[s.getpeername()].send_msg()
        for s in exceptional:
            print "exception condition on ", s.getpeername()
            self.close_connection(s)

    def init_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setblocking(False)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_address = ('', 9998)
        server.bind(server_address)
        server.listen(100)
        self.server = server

    def __init__(self):
        self.server = None
        self.init_server()
        self.clients = {}
        self.inputs = [self.server]
        self.outputs = []
        self.timeout = 2
        while self.inputs:
            self.mainloop()


