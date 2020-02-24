import odrive
from odrive.enums import *
import time

od = odrive.find_any()
if od.serial_number == 59877000491063:
    print("found odrive 1")
    od.axis0.motor.config.calibration_current = 15.0
    od.axis0.motor.config.current_lim = 40.0
    od.axis0.motor.config.requested_current_range = 60.0

    od.axis0.requested_state = AXIS_STATE_MOTOR_CALIBRATION
    time.sleep(32)
    print("axis error: " + str(od.axis0.error))
    print("motor error: " + str(od.axis0.motor.error))
    print("encoder error: " + str(od.axis0.encoder.error))
    print("controller error: " + str(od.axis0.controller.error))

    od.axis1.motor.config.calibration_current = 15.0
    od.axis1.motor.config.current_lim = 40.0
    od.axis1.motor.config.requested_current_range = 60.0

    od.axis1.requested_state = AXIS_STATE_MOTOR_CALIBRATION
    time.sleep(32)
    print("axis error: " + str(od.axis1.error))
    print("motor error: " + str(od.axis1.motor.error))
    print("encoder error: " + str(od.axis1.encoder.error))
    print("controller error: " + str(od.axis1.controller.error))

elif od.serial_number == 35623325151307:
    print("found odrive 2")
    od.axis0.motor.config.calibration_current = 15.0
    od.axis0.motor.config.current_lim = 40.0
    od.axis0.motor.config.requested_current_range = 60.0
 
    od.axis0.requested_state = AXIS_STATE_MOTOR_CALIBRATION
    time.sleep(32)
    print("axis error: " + str(od.axis0.error))
    print("motor error: " + str(od.axis0.motor.error))
    print("encoder error: " + str(od.axis0.encoder.error))
    print("controller error: " + str(od.axis0.controller.error))
od.reboot()
