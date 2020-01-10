import time

import odrive
import usb.core
from odrive.enums import *
from fibre.protocol import ChannelBrokenException

def reboot_odrive():
    try:
        od.save_configuration()
        od.reboot()
    except ChannelBrokenException:
        print('motor calibration complete')
        exit(0)

calibrating = 0

od = odrive.find_any()

print("odrive found: " + str(od.serial_number))
time.sleep(2)

if od.axis0.motor.config.pre_calibrated:
    print("The motor is already calibrated, setting pre_calibrated to false. Please rerun this script")
    od.axis0.motor.config.pre_calibrated = False
    reboot_odrive()

if calibrating == 0:
    od.axis0.requested_state = AXIS_STATE_MOTOR_CALIBRATION
if calibrating == 1:
    od.axis1.requested_state = AXIS_STATE_MOTOR_CALIBRATION

print('motor calibrated')

time.sleep(2)
if calibrating == 0:
    od.axis0.motor.config.pre_calibrated = True
if calibrating == 1:
    od.axis1.motor.config.pre_calibrated = True


print('configuration saved')
time.sleep(2)

reboot_odrive()



