from threading import Thread
import enum
from common import *
import socket
import time

class PacketType(enum.Enum):
    NULL = 0
    COMMAND1 = 1
    COMMAND2 = 2

class Server():

    def __init__(self):

        self.stopped = False
        self.instructions_list = []
        self.client_ready = False
        self.restart = False
        self.server = None
        self.connection = None
        self.packet_enum = PacketType
        self.dead = False
        self.deadbeat = .5
        self.retry = 4
        #self.storedPacket = []

    def open_server(self):
        self.server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
        self.server.bind(("127.0.0.1", 5001))
        self.server.listen(1)

    def wait_for_connection(self):
        if self.connection is not None:
            raise RuntimeError("A connection has already been established; use reconnect() to reconnect.")
        self.reconnect()

    def reconnect(self):
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
        #print("SERVER: sent " + str(payload))

    def recv_packet(self):
        return recv_packet(self.connection, self.packet_enum)
    
    def checkAlive(self):
        return self.dead

    def send(self, instructions_list):
        self.instructions_list = instructions_list

    def run(self):
        Thread(target=self.update, args=()).start()
        Thread(target=self.serverBeat, args=()).start()
        return self

    def stop(self):
        self.stopped = True
        print("stopped = True")

    def update(self):
        self.open_server()
        print("SERVER: waiting for connection")
        self.wait_for_connection()
        print("SERVER: connected")
        # send command2, receive command 1
        while not self.stopped:
            if self.client_ready:
                if len(self.instructions_list) != 0:
                    for instruction in self.instructions_list:
                        if instruction == "rotateLeft":
                            self.send_packet(PacketType.COMMAND2, b"rotateLeft")
                        elif instruction == "rotateRight":
                            self.send_packet(PacketType.COMMAND2, b"rotateRight")
                        elif instruction == "forwards":
                            self.send_packet(PacketType.COMMAND2, b"forwards")
                        elif instruction == "backwards":
                            self.send_packet(PacketType.COMMAND2, b"backwards")
                        elif instruction == "1":
                            self.send_packet(PacketType.COMMAND2, b"1")
                        elif instruction == "2":
                            self.send_packet(PacketType.COMMAND2, b"2")
                        elif instruction == "3":
                            self.send_packet(PacketType.COMMAND2, b"3")
                        elif instruction == "newGame":
                            self.send_packet(PacketType.COMMAND2, b"newGame")
                    self.send_packet(PacketType.COMMAND2, b"end")
                    self.instructions_list = []
                    self.client_ready = False
            else:
                '''
                if self.storedPacket:
                    print("SERVER: accessing stored packet")
                    packet = self.storedPacket[0]
                    self.storedPacket.remove(packet)
                else:
                '''
                packet = self.recv_packet()
                print("SERVER: received packet: " + str(packet))
                if packet == (PacketType.COMMAND1, b"ready"):
                    self.client_ready = True
                elif packet == (PacketType.COMMAND1, b"restart"):
                    self.restart = True
                    self.client_ready = True

        self.send_packet(PacketType.COMMAND2, b"shutdown")
        self.close_connection()
        print("SERVER: connection closed")
        self.close_server()
        print("SERVER: server closed")
        self.dead = True

    def serverBeat(self):
        print("SERVER: starting serverBeat")
        while self.connection is None:
            pass
        self.send_packet(PacketType.COMMAND2, b"serverBeat")
        while not self.stopped:
            packet = self.recv_packet()
            if packet:
                if packet == (PacketType.COMMAND1, b"clientBeat"):
                    print("SERVER: serverBeat received " + str(packet))
                    self.retry = 4
                    self.send_packet(PacketType.COMMAND2, b"serverBeat")
                else:
                    print("SERVER: stored packet:" + str(packet))
                    #self.storedPacket.append(packet)
            else:
                self.retry -= 1
                print("SERVER: retry at " + str(self.retry))
                if self.retry == 0:
                    self.stopped = True
            time.sleep(self.deadbeat)
            print("SERVER: testing serverBeat, retry at " + str(self.retry))
        print("SERVER: shutting down serverBeat")

class Client():
     
    def __init__(self):
        self.stopped = False
        self.ready = False
        self.change_ready = False
        self.instructions = []
        self.instructions_ready = False
        self.restart = False
        self.connection = None
        self.packet_enum = PacketType
        self.deadbeat = .5
        self.dead = False
        self.retry = 4
        self.heartbeat1 = time.time()
        self.heartbeat2 = time.time()

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
        self.connection.connect(("127.0.0.1", 5001))

    def close_connection(self):
        self.connection.close()

    def send_packet(self, packet_type, payload):
        send_packet(self.connection, packet_type, payload)
        #print("CLIENT: sent " + str(payload))

    def recv_packet(self):
        return recv_packet(self.connection, self.packet_enum)

    def run(self):
        Thread(target=self.update, args=()).start()
        #Thread(target=self.clientBeat, args=()).start()
        return self

    def getInstructions(self):
        if self.instructions_ready:
            return self.instructions
        else:
            return False
   
    def checkAlive(self):
        return self.dead
   
    def makeReady(self):
        self.instructions = []
        self.instructions_ready = False
        self.change_ready = True

    def stop(self):
        self.stopped = True

    def update(self):
        print("CLIENT: waiting for a connection")
        self.connect()
        print("CLIENT: connected")
        # send the ready flag
        # send command1, receive command2
        self.ready = True
        self.send_packet(PacketType.COMMAND1, b"ready")

        while not self.stopped:
            # receive commands from server
            if self.ready:
                packet = self.recv_packet()
                print("CLIENT: received " + str(packet))
                if packet == (PacketType.COMMAND2, b"rotateLeft"):
                    self.instructions.append("rotateLeft")
                elif packet == (PacketType.COMMAND2, b"rotateRight"):
                    self.instructions.append("rotateRight")
                elif packet == (PacketType.COMMAND2, b"forwards"):
                    self.instructions.append("forwards")
                elif packet == (PacketType.COMMAND2, b"backwards"):
                    self.instructions.append("backwards")
                elif packet == (PacketType.COMMAND2, b"end"):
                    self.ready = False
                    self.instructions_ready = True
                elif packet == (PacketType.COMMAND2, b"shutdown"):
                    self.stopped = True
                elif packet == (PacketType.COMMAND2, b"1"):
                    self.instructions.append("1")
                elif packet == (PacketType.COMMAND2, b"2"):
                    self.instructions.append("2")
                elif packet == (PacketType.COMMAND2, b"3"):
                    self.instructions.append("3")
                elif packet == (PacketType.COMMAND2, b"newGame"):
                    print("received newGame command")
                    self.instructions.append("newGame")
                elif packet == (PacketType.COMMAND2, b"serverBeat"):
                    self.retry = 4
                    self.send_packet(PacketType.COMMAND1, b"clientBeat")

            else:
                if self.change_ready:
                    if self.restart:
                        self.send_packet(PacketType.COMMAND1, b"restart")
                        self.ready = True
                        self.restart = False
                        self.change_ready = False
                    else:
                        self.send_packet(PacketType.COMMAND1, b"ready")
                        self.ready = True
                        self.change_ready = False
            self.heartbeat2 = time.time()
            elapsed = self.heartbeat2 - self.heartbeat1
            print("CLIENT: time elapsed: " + str(elapsed))
            if self.retry == 0:
                self.stopped = True
                print("CLIENT: retry at 0")
            elif elapsed >= .5:
                self.retry -= 1
                self.heartbeat1 = self.heartbeat2
            print("CLIENT: retry at: " + str(self.retry))
        self.close_connection()
        self.dead = True
