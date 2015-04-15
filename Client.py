import json
from encoder import MyEncoder


class Client:
    def __init__(self, peername, connection):
        from Queue import Queue
        self.peername = peername
        self.connection = connection
        self.user = None
        self.msgs = Queue()

    def handle_msg(self, server, raw_msg):
        msg = json.loads(raw_msg)
        header = msg['header']
        if header == 'register':
            pass
        elif header == 'unregister':
            pass
        elif header == 'get_slaves':
            r_msg = self.get_slaves(server)
        self.msgs.put_nowait(r_msg)

    def get_slaves(self, server):
        return {'data': server.slaves}

    def send_msg(self):
        try:
            msg = self.msgs.get_nowait()
            self.connection.send(msg)
        except:
            print "send msg error"

    def clean(self):
        pass

