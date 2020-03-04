import odrive
from odrive.enums import *
from RPi_ODrive import ODrive_Ease_Lib
import time

od = odrive.find_any()
if od.serial_number == 59877000491063:
    print("found odrive 1")
    od.axis0.motor.config.calibration_current = 15.0
    od.axis0.motor.config.current_lim = 40.0
    od.axis0.motor.config.requested_current_range = 60.0

    print("starting motor 1")
    ax0 = ODrive_Ease_Lib.ODrive_Axis(od.axis0)
    ax0.index_and_hold(-1, 1)
    print("waiting")
    time.sleep(10)

    print("axis error: " + str(od.axis0.error))
    print("motor error: " + str(od.axis0.motor.error))
    print("encoder error: " + str(od.axis0.encoder.error))
    print("controller error: " + str(od.axis0.controller.error))
    od.axis1.motor.config.calibration_current = 15.0
    od.axis1.motor.config.current_lim = 40.0
    od.axis1.motor.config.requested_current_range = 60.0
    
    print("starting motor 2")
    ax1 = ODrive_Ease_Lib.ODrive_Axis(od.axis1)
    ax1.index_and_hold(-1, 1)
    print("waiting")
    time.sleep(10)

    print("axis error: " + str(od.axis1.error))
    print("motor error: " + str(od.axis1.motor.error))
    print("encoder error: " + str(od.axis1.encoder.error))
    print("controller error: " + str(od.axis1.controller.error))
    

elif od.serial_number == 35623325151307:
    print("found odrive 2")
    od.axis0.motor.config.calibration_current = 15.0
    od.axis0.motor.config.current_lim = 40.0
    od.axis0.motor.config.requested_current_range = 60.0
 
    print("starting motor 3")
    ax2 = ODrive_Ease_Lib.ODrive_Axis(od.axis0)
    ax2.index_and_hold(-1, 1)
    time.sleep(32)
    print("waiting")
    time.sleep(10)

    print("axis error: " + str(od.axis0.error))
    print("motor error: " + str(od.axis0.motor.error))
    print("encoder error: " + str(od.axis0.encoder.error))
    print("controller error: " + str(od.axis0.controller.error))

print("shutting down in 5 seconds")
time.sleep(5)
od.reboot()
