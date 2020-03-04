# minimalistic script to test API functionality
# Braedan Kennedy (Dec 2, 2019) V.2

import os
import spidev
from pidev.Cyprus_Commands import Cyprus_Commands_RPi as cyprus
import time


# setup limit switches and solenoid
spi = spidev.SpiDev()
cyprus.initialize()
version = cyprus.read_firmware_version()
print("Found CyPrus, Firmware version: ", version)



def getProx():
    if (cyprus.read_gpio() & 0b1000):
        return False
    else:
        return True

try:
    while 1:
        print(getProx())
except:
    pass


print("shutoff in 5 seconds")
time.sleep(5)
exit()
