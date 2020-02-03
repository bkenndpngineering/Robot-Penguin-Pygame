from threading import Thread
from packetType import PacketType
from dpea_p2p import Server, Client

class gameServer():
    def __init__(self, IP="172.17.21.1", port=9999):
        self.server = Server(IP, port, PacketType)  # IP, port, packet-type
        self.stopped = False
        self.instructions_list = []
        self.client_ready = False
        self.restart = False

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
                        if instruction == "rotateLeft":
                            self.server.send_packet(PacketType.COMMAND2, b"rotateLeft")
                        elif instruction == "rotateRight":
                            self.server.send_packet(PacketType.COMMAND2, b"rotateRight")
                        elif instruction == "forwards":
                            self.server.send_packet(PacketType.COMMAND2, b"forwards")
                        elif instruction == "backwards":
                            self.server.send_packet(PacketType.COMMAND2, b"backwards")
                        elif instruction == "1":
                            self.server.send_packet(PacketType.COMMAND2, b"1")
                        elif instruction == "2":
                            self.server.send_packet(PacketType.COMMAND2, b"2")
                        elif instruction == "3":
                            self.server.send_packet(PacketType.COMMAND2, b"3")
                        elif instruction == "newGame":
                            self.server.send_packet(PacketType.COMMAND2, b"newGame")
                    self.server.send_packet(PacketType.COMMAND2, b"end")
                    self.instructions_list = []
                    self.client_ready = False
            else:
                packet = self.server.recv_packet()
                print(packet)
                if packet == (PacketType.COMMAND1, b"ready"):
                    self.client_ready = True
                elif packet == (PacketType.COMMAND1, b"restart"):
                    self.restart = True
                    self.client_ready = True

        self.server.send_packet(PacketType.COMMAND2, b"shutdown")
        self.server.close_connection()
        self.server.close_server()

class gameClient():
    def __init__(self, IP="172.17.21.1", port=9999):
        self.client = Client(IP, port, PacketType)
        self.stopped = False
        self.ready = False
        self.change_ready = False
        self.instructions = []
        self.instructions_ready = False
        self.restart = False

    def run(self):
        Thread(target=self.update, args=()).start()
        return self

    def getInstructions(self):
        if self.instructions_ready:
            return self.instructions
        else:
            return False

    def makeReady(self):
        self.instructions = []
        self.instructions_ready = False
        self.change_ready = True

    #def resetSignal(self):
    #    self.instructions = []
    #    self.instructions_ready = False
    #    self.change_ready = False
    #    self.restart = True

    def stop(self):
        self.stopped = True

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
                    self.ready = False
                    self.makeReady()

            else:
                if self.change_ready:
                    if self.restart:
                        self.client.send_packet(PacketType.COMMAND1, b"restart")
                        self.ready = True
                        self.restart = False
                        self.change_ready = False
                    else:
                        self.client.send_packet(PacketType.COMMAND1, b"ready")
                        self.ready = True
                        self.change_ready = False


        # needs to time out or something. waits forever for a packet
        self.client.close_connection()