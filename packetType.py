import enum

# packet type to be used for client/server communication

class PacketType(enum.Enum):
    NULL = 0
    #INSTRUCTION_LEFT = 1
    #INSTRUCTION_RIGHT = 2
    #INSTRUCTION_UP = 3
    #INSTRUCTION_DOWN = 4
    #SHUTDOWN = 5
    #READY = 6
    COMMAND1 = 1
    COMMAND2 = 2