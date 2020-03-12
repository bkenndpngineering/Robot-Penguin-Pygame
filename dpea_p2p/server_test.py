from commPoll import PacketType, Server

s = Server()
s.run()
s.instruction_list = [1]
s.send(instruction_list)
s.stop()
