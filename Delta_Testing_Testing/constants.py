# constants file
# contains measurements from SolidWorks about the dimensions of the DPEA Delta arm
# measurements taken by Joseph Pearlman and Charly Parker

# base to motor AKA base radius
f = 121.44  # millimeters

# motor to elbow AKA bicep length
rf = 307.83 # millimeters

# elbow to wrist AKA forearm length
re = 616.58 # millimeters

# wrist to tool AKA end effector radius
e = 62.59

# end effector z offset
z0 = 0


####### Extra Constants #######
DEG_TO_STEPS = 6400/360         # for the stepper motor

ENCODER_CPR = 8192

CPR_TO_DEG = 360/ENCODER_CPR
DEG_TO_CPR = ENCODER_CPR/360

from math import radians
phi_vals = [radians(210), radians(90), radians(330)]

