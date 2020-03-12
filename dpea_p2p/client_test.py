from commPoll import PacketType, Client

c = Client()
c.run()
while not c.instructions:
    pass
print("CLIENT: received " + str(c.instructions))
c.makeReady()
