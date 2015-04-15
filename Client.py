class Client:

    def __init__(self, peername, connection):
        from Queue import Queue
        self.peername = peername
        self.connection = connection
        self.user = None
        self.msgs = Queue()

    def handle_msg(self, msg):
        pass

    def send_msg(self):
        try:
            msg = self.msgs.get_nowait()
            self.connection.send(msg)
        except:
            print "send msg error"

    def clean(self):
        pass

