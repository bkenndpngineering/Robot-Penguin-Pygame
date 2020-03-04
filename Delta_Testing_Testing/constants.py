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
TOF_HORIZONTAL_OFFSET = 60
# distance from top of arm to sensor when the arm is horizontal in millimeters - distanc
TOF_VERTICAL_OFFSET = 45


######## ODrive Motor Configuration ########