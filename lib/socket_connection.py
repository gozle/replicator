import socket
import struct

__all__ = ["Connection", "recv_all", "recv", "send", "address_to_tuple"]


class Connection(socket.socket):

    def __init__(self, addr=None):
        super().__init__()
        self.addr = addr

    def connect(self, *args, **kwargs):
        return super().connect(self.addr)

    def start(self):
        self.bind_()
        self.listen_()

    def listen_(self):
        self.listen()
        print("[SERVER] listening...", self.addr)

    def bind_(self):
        self.bind(self.addr)
        print("[SERVER] binded to", self.addr)

    def recv_all_(self):
        raw_msglen = self.recv_(8)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>Q', raw_msglen)[0]
        return self.recv_(msglen)

    def recv_(self, n):
        data = bytearray()
        while len(data) < n:
            packet = self.recv(n - len(data))
            if not packet:
                return None
            data.extend(packet)
        return data

    def send_(self, msg, encode=True):
        if encode:
            msg = msg.encode()
        msg = struct.pack('>Q', len(msg)) + msg
        self.sendall(msg)


def address_to_tuple(address):
    addr = address.split(':')
    return addr[0], int(addr[1])


def recv_all(conn):
    raw_msglen = recv(conn, 8)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>Q', raw_msglen)[0]
    return recv(conn, msglen)


def recv(conn, n):
    data = bytearray()
    while len(data) < n:
        packet = conn.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data


def send(conn, msg, encode=True):
    if encode:
        msg = msg.encode()
    msg = struct.pack('>Q', len(msg)) + msg
    conn.sendall(msg)
