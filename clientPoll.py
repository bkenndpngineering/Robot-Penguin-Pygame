from threading import Thread
from packetType import PacketType
from dpea_p2p import Server, Client

class gameServer():
    def __init__(self, IP="127.0.0.1", port=9999):
        self.server = Server(IP, port, PacketType)  # IP, port, packet-type
        self.stopped = False
        self.instructions_list = []
        self.client_ready = False

    def send(self, instructions_list):
        self.instructions_list = instructions_list

    def run(self):
        Thread(target=self.update, args=()).start()
        return self

    def stop(self):
        self.stopped = True

    def update(self):
        self.server.open_server()
        print("SERVER: waiting for connection")
        self.server.wait_for_connection()
        print("SERVER: connected")
        # send command2, receive command 1
        while not self.stopped:
            if self.client_ready:
                if len(self.instructions_list) != 0:
                    for instruction in self.instructions_list:
                        if instruction == "left":
                            self.server.send_packet(PacketType.COMMAND2, b"left")
                        elif instruction == "right":
                            self.server.send_packet(PacketType.COMMAND2, b"right")
                        elif instruction == "up":
                            self.server.send_packet(PacketType.COMMAND2, b"up")
                        elif instruction == "down":
                            self.server.send_packet(PacketType.COMMAND2, b"down")
                    self.server.send_packet(PacketType.COMMAND2, b"end")
                    self.instructions_list = []
                    self.client_ready = False
            else:
                packet = self.server.recv_packet()
                print(packet)
                if packet == (PacketType.COMMAND1, b"ready"):
                    self.client_ready = True

        self.server.close_connection()
        self.server.close_server()

class gameClient():
    def __init__(self, IP="127.0.0.1", port=9999):
        self.client = Client("127.0.0.1", 9999, PacketType)
        self.stopped = False
        self.ready = False
        self.change_ready = False
        self.instructions = []
        self.instructions_ready = False

    def run(self):
        Thread(target=self.update, args=()).start()
        return self

    def stop(self):
        self.stopped = True

    def getInstructions(self):
        if self.instructions_ready:
            return self.instructions
        else:
            return False

    def makeReady(self):
        self.instructions = []
        self.instructions_ready = False
        self.change_ready = True

    def update(self):
        print("CLIENT: waiting for a connection")
        self.client.connect()
        print("CLIENT: connected")
        # send the ready flag
        # send command1, receive command2
        self.ready = True
        self.client.send_packet(PacketType.COMMAND1, b"ready")

        while not self.stopped:
            # receive commands from server
            if self.ready:
                packet = self.client.recv_packet()
                print(packet)
                if packet == (PacketType.COMMAND2, b"left"):
                    self.instructions.append("left")
                elif packet == (PacketType.COMMAND2, b"right"):
                    self.instructions.append("right")
                elif packet == (PacketType.COMMAND2, b"up"):
                    self.instructions.append("up")
                elif packet == (PacketType.COMMAND2, b"down"):
                    self.instructions.append("down")
                elif packet == (PacketType.COMMAND2, b"end"):
                    self.ready = False
                    self.instructions_ready = True
            else:
                if self.change_ready:
                    self.client.send_packet(PacketType.COMMAND1, b"ready")
                    self.ready = True

        # needs to time out or something. waits forever for a packet
        self.client.close_connection()