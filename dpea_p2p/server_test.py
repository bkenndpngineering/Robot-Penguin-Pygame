from commPoll import Server
import time
s = Server()
s.run()
while not s.client_ready:
    pass
'''
instruction_list = ["1"]
s.send(instruction_list)
time.sleep(2)
for i in range(0,3):
    instruction_list = ["rotateLeft", "rotateLeft", "forwards", "forwards"]
    s.send(instruction_list)
    time.sleep(2)
'''
time.sleep(10)
s.stop()
