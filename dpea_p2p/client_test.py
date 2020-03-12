from commPoll import PacketType, Client
import time

c = Client()
c.run()
while not c.stopped:
    c.makeReady()
    time.sleep(.5)
