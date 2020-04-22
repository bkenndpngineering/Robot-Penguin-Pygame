from commPoll import Client
import time

c = Client()
c.run()
#for d in range(0,4):
while not c.stopped:
    c.makeReady()
    time.sleep(.5)
#c.stop()
