from commPoll import PacketType, Server
import time
s = Server()
s.run()
while not s.client_ready:
    pass
instruction_list = ["1"]
s.send(instruction_list)
time.sleep(2)
print("sending stop")
s.stop()
print("sent stop")
