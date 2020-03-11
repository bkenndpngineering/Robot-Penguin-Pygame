from threading import Thread
from packetType import PacketType
from .common import *
import socket

class PacketType(enum.Enum):
    NULL = 0
    COMMAND1 = 1
    COMMAND2 = 2

#         |Bind IP       |Port |Packet enum
s = Server("172.17.21.2", 5001, PacketType)
s.open_server()
s.wait_for_connection()
s.recv_packet() == (PacketType.COMMAND1, b"Hello!")
s.send_packet(PacketType.COMMAND2, b"Hello back!")
s.close_connection()
s.close_server()

class Server():

    def __init__(self):

        pass

    def open_server(self):
        self.server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.server.bind((127.0.0.1, 5001))
        self.server.listen(1)

    def wait_for_connection(self):
        if self.connection is not None:
            raise RuntimeError("A connection has already been established; use reconnect() to reconnect.")
        self.reconnect()

    def reconect(self):
        if self.connection is not None:
            try:
                self.close_connection()
            except OSError:
                pass
        conn, addr = self.server.accept()
        self.connection = conn

    def close_connection(self):
        self.connection.close()

    def close_server(self):
        self.server.close()

    def send_packet(self, packet_type, payload):
        send_packet(self.connection, packet_type, payload)

    def recv_packet(self):
        return recv_packet(self.connection, self.packet_enum)

class Client():
     
    def __init__(self):
        pass

    def connect(self):
        if self.connection is not None:
            raise RuntimeError("A connection has already been established; use reconnect() to reconnect.")
        self.reconnect()

    def reconnect(self):
        if self.connection is not None:
            try:
                self.close_connection()
            except OSError:
                pass
        self.connection = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.connection.connect((127.0.0.1, 5001))

    def close_connection(self):
        self.connection.close()

    def send_packet(self, packet_type, payload):
        send_packet(self.connection, packet_type, payload)

    def recv_packet(self):
        return recv_packet(self.connection, self.packet_enum)


