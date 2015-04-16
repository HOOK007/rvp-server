import json


class Client:
    def __init__(self, server, peername, connection):
        from Queue import Queue
        self.peername = peername
        self.connection = connection
        self.udp_addr = None
        self.user = None
        self.msgs = Queue()
        self.server = server

    def handle_msg(self, raw_msg):
        msg = json.loads(raw_msg)
        req = msg['req']
        if req == 'register':
            r_msg = self.register(msg)
        elif req == 'unregister':
            r_msg = self.unregister()
        elif req == 'get_slaves':
            r_msg = self.get_slaves()
        else:
            r_msg = {'resp': "error"}
        self.msgs.put_nowait(json.dumps(r_msg))

    def get_slaves(self):
        return {
            'resp': 'slaves',
            'data': self.server.META['slaves']
        }

    def register(self, msg):
        self.udp_addr = msg['address']
        self.server.META['slaves'].append(msg['address'])
        return {
            'resp': 'register',
            'ans': 'success',
        }

    def unregister(self):
        try:
            self.server.META['slaves'].remove(self.udp_addr)
        except Exception, e:
            print e.message
        return {
            'resp': 'unregister',
            'ans': 'success',
        }

    def send_msg(self):
        try:
            msg = self.msgs.get_nowait()
            self.connection.send(msg)
        except Exception, e:
            print e.message
            print "send msg error", msg

    def clean(self):
        self.unregister()
        self.connection.close()

