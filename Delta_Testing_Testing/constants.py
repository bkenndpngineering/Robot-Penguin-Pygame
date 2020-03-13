# constants file
# contains measurements from SolidWorks about the dimensions of the DPEA Delta arm
# measurements taken by Joseph Pearlman and Charlie Parker

# base to motor AKA base radius
f = 80.9 #121.44 millimeters

# motor to elbow AKA bicep length
rf = 304.8 #307.83 millimeters

# elbow to wrist AKA forearm length
re = 616.58 #millimeters

# wrist to tool AKA end effector radius
e = 66.17 #62.59

# end effector z offset
z0 = 0


####### Kinetmatic Constants #######

DEG_TO_STEPS = 400/360         # for the stepper motor
# 200 steps per revolution * microstepping count

ENCODER_CPR = 8192

CPR_TO_DEG = 360/ENCODER_CPR
DEG_TO_CPR = ENCODER_CPR/360

from math import radians
phi_vals = [radians(210), radians(90), radians(330)]


######## TOF sensor constants ########

# horizontal distance from sensor to motor axle in millimeters
TOF_HORIZONTAL_OFFSET = 80
# distance from top of arm to sensor when the arm is horizontal in millimeters - distance
TOF_VERTICAL_OFFSET = 33
# Weighted Moving Average filter array length, how many sensor readings are stored
WMA_ARRAY_LENGTH = 10
# I2C Multiplexer address - TCA9548A - default 0x70, could be any from 0x70 to 0x77
import smbus
__bus = smbus.SMBus(1)
__addresses = []
for device in range(128):
    try:
        __bus.read_byte(device)
        print(hex(device))
       __ addresses.append(hex(device))
    except:
        pass
if (len(__addresses) != 0):
    __last_address = __addresses[len(__addresses)-1]
    if (__last_address > 0x69):
        TCA9548A_ADDRESS = __last_address
    else:
        TCA9548A_ADDRESS = None
TCA9548A_ADDRESS = None
del __bus

######## ODrive Motor Configuration ########

# default
# pos_gain = 0.1
# vel_gain = 0.02
# vel_integrator_gain = 0.1

ODRIVE_CONFIG_VARS =    {
                        "pos_gain": 4.0,
                        "vel_gain": 0.01,
                        "vel_integrator_gain": 0.1,
                        "calibration_current": 15.0,
                        "current_limit": 40.0,
                        "current_control_bandwidth": 100.0,
                        "requested_current_range": 60.0,
                        "pole_pairs": 15,
                        "encoder_cpr": ENCODER_CPR
                        }

