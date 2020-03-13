from commPoll import Client
import time

c = Client()
c.run()
for d in range(0,4):
    c.makeReady()
    time.sleep(.5)
c.stop()
