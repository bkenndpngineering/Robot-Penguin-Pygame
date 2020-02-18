from Delta_Testing_Testing.deltaArm import DeltaArm
from odrive.enums import *
import time

arm = DeltaArm()

if not arm.initialize():
    exit()

arm.ax0.axis.requested_state = AXIS_STATE_IDLE
arm.ax1.axis.requested_state = AXIS_STATE_IDLE
arm.ax2.axis.requested_state = AXIS_STATE_IDLE
state = False
while 1:
    print(arm.getHomedCoordinates())
