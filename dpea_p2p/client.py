"""
This module contains the Client class that manages a connection to a dpea-p2p server.

General usage looks like this:

```
class PacketType(enum.Enum):
    NULL = 0
    COMMAND1 = 1
    COMMAND2 = 2

#         |Server IP     |Port |Packet enum
c = Client("172.17.21.2", 5001, PacketType)
c.connect()

c.send_packet(PacketType.COMMAND1, b"Hello!")
c.recv_packet() == (PacketType.COMMAND2, b"Hello back!")

c.close_connection()
```
"""

from .common import *
import socket


class Client(object):
    """
    A class that manages the state of a connection to a dpea-p2p server.

    Upon calling .connect(), it connects to server_ip:server_port.
    It interprets received packet types via packet_enum.

    .send_packet() and .recv_packet() allow for communication.

    When the connection is finished, call .close_connection().
    """

    def __init__(self, server_ip, server_port, packet_enum):
        """
        Initializes the client.

        :param server_ip: The IP address of the server to connect to.
        :param server_port: The port of the server to connect to.
        :param packet_enum: The enum containing the packet types.
        :returns: A new Client object.
        """
        self.server_ip = server_ip
        self.server_port = server_port
        self.packet_enum = packet_enum

        self.connection = None

    # Connection helpers

    def connect(self):
        """
        Attempts a connection to the remote server.
        This function will throw an error if a connection has previously been established.
        If _reconnection_ is desired, use .reconnect().

        :raises RuntimeError: If a connection has already been established.
        """
        if self.connection is not None:
            raise RuntimeError("A connection has already been established; use reconnect() to reconnect.")
        self.reconnect()

    def reconnect(self):
        """
        Attempts a connection to the remote server, regardless of any previous connections.
        """
        if self.connection is not None:
            try:
                self.close_connection()
            except OSError:
                pass
        self.connection = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.connection.connect((self.server_ip, self.server_port))

    def close_connection(self):
        """
        Closes the connection to the remote.
        """
        self.connection.close()

    # Send/recv

    def send_packet(self, packet_type, payload):
        """
        Sends a packet to the server.

        :param packet_type: Either an int or an enum value representing the packet type.
        :param payload: The payload to be sent. Should be a bytes-like object.
        """
        send_packet(self.connection, packet_type, payload)

    def recv_packet(self):
        """
        Receives a packet from the server.

        :returns: A tuple of (packet_type, payload) from the server.
        """
        return recv_packet(self.connection, self.packet_enum)
