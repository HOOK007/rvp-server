class XqlUser:
    def __init__(self, username, addr, other=None):
        self.username = username
        self.tcpAddr = addr
        self.udpAddr = 0
        self.other = other
        self.alive = 0

