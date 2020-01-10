import os
import spidev
from pidev.stepper import stepper
from pidev.Cyprus_Commands import Cyprus_Commands_RPi as cyprus
from Slush.Devices import L6470Registers
import odrive
from RPi_ODrive import ODrive_Ease_Lib
import RPi.GPIO as GPIO
from kinematicFunctions import *
import time

"""
DeltaArm API V.3 (Dec 2, 2019) by Braedan Kennedy (bkenndpngineering)
Supplemental development by Joseph Pearman and Philip Nordblad

for use with the DPEA Robot Penguin project
modules can be used for any Delta Arm project
"""

class DeltaArm():
    def __init__(self):
        self.initialized = False    # if the arm is not initialized no motor related commands will work. represents the ODrive harware
        
        self.spi = None             # spidev
        self.stepper = None         # stepper motor object

        self.ODriveSerialNumber1 = 59877000491063   # first ODrive serial number. Controls motors 1 and 2
        self.ODriveSerialNumber2 = 35623325151307   # second ODrive serial number. Controls motor 3

        self.od1 = None             # first ODrive instance
        self.od2 = None             # second ODrive instance

        self.ax0 = None             # axis 0 of the first ODrive. Motor 1
        self.ax1 = None             # axis 1 of the first ODrive. Motor 2
        self.ax2 = None             # axis 0 of the second ODrive. Motor 3

        self.homedCoordinates = None  # coordinates of the home position, use for relative movement

    def rotateStepper(self, degree):
        # rotate stepper motor shaft in degrees
        if self.initialized:
            steps = degree * DEG_TO_STEPS
            self.stepper.relative_move(steps)

    def powerSolenoid(self, state):
        # Written by Joseph Pearlman and Philip Nordblad
        # toggle solenoid on and off
        if self.initialized:
            if state == True:
                cyprus.set_pwm_values(1, period_value=100000, compare_value=500000, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
            elif state == False:
                cyprus.set_pwm_values(1, period_value=100000, compare_value=0, compare_mode=cyprus.LESS_THAN_OR_EQUAL)
            else:
                return

    def getLim1(self):
        # return status of limit switch 1, of motor 1
        if (cyprus.read_gpio() & 0b0001):
            return False
        else:
            return True

    def getLim2(self):
        # return status of limit switch 2, of motor 2
        if (cyprus.read_gpio() & 0b0010):
            return False
        else:
            return True

    def getLim3(self):
        # return status of limit switch 3, of motor 3
        if (cyprus.read_gpio() & 0b0100):
            return False
        else:
            return True

    def connectODrive(self):
        # find two ODrives and assign them to the correct motors
        # returns false if there is not two ODrives connected or their serial numbers do not match those defined above
        o = ODrive_Ease_Lib.find_ODrives()
        if len(o) != 2:
            return False
        
        if o[0].serial_number == self.ODriveSerialNumber1: od1 = o[0]
        elif o[0].serial_number == self.ODriveSeriaNumber2: od2 = o[0]
        else: return False

        if o[1].serial_number == self.ODriveSerialNumber1: od1 = o[1]
        elif o[1].serial_number == self.ODriveSerialNumber2: od2 = o[1]
        else: return False

        # preserve ODrive object for shutdown method
        self.od1 = od1
        self.od2 = od2

        # initialize ODrive motor axis
        self.ax0 = ODrive_Ease_Lib.ODrive_Axis(od1.axis0)
        self.ax1 = ODrive_Ease_Lib.ODrive_Axis(od1.axis1)
        self.ax2 = ODrive_Ease_Lib.ODrive_Axis(od2.axis0)

        return True

    def homeMotors(self):
        # move the motors to index position. Requirement for position control
        self.ax0.index_and_hold(-1, 1)
        time.sleep(1)
        self.ax1.index_and_hold(-1, 1)
        time.sleep(1)
        self.ax2.index_and_hold(-1, 1)
        time.sleep(1)

        # home motor 1
        self.ax0.set_vel(-20)
        while (not self.getLim1()):
            continue
        self.ax0.set_vel(0)
        self.ax0.set_home()
        time.sleep(1)

        # home motor 2
        self.ax1.set_vel(-20)
        while (not self.getLim2()):
            continue
        self.ax1.set_vel(0)
        self.ax1.set_home()
        time.sleep(1)

        # home motor 3
        self.ax2.set_vel(-20)
        while (not self.getLim3()):
            continue
        self.ax2.set_vel(0)
        self.ax2.set_home()
        time.sleep(1)

        # if anything is wrong with ODrive, the homing sequence will be registered as a failure
        if self.ax0.axis.error != 0: return False
        if self.ax0.axis.motor.error != 0: return False
        if self.ax0.axis.encoder.error != 0: return False
        if self.ax0.axis.controller.error != 0: return False

        if self.ax1.axis.error != 0: return False
        if self.ax1.axis.motor.error != 0: return False
        if self.ax1.axis.encoder.error != 0: return False
        if self.ax1.axis.controller.error != 0: return False
        
        if self.ax2.axis.error != 0: return False
        if self.ax2.axis.motor.error != 0: return False
        if self.ax2.axis.encoder.error != 0: return False
        if self.ax2.axis.controller.error != 0: return False

        return True

    def initialize(self):
        # returns true is successful, false if not
        # setup limit switches and solenoid
        self.spi = spidev.SpiDev()
        cyprus.initialize()
        version = cyprus.read_firmware_version()
        print("Found CyPrus, Firmware version: ", version)

        # connect to ODrives
        ODriveConnected = self.connectODrive()

        if (ODriveConnected == True):
            # if GPIO and ODrive are setup properly, attempt to home
            HomedMotors = self.homeMotors()
            if (HomedMotors == True): self.initialized = True

        if self.initialized:
            # calculate homed coordinates
            self.homedCoordinates = self.getCoordinates()

            # setup and home stepper
            self.stepper = stepper(port=0, micro_steps=32, hold_current=40, run_current=40, accel_current=40,
                                   deaccel_current=40, steps_per_unit=200,
                                   speed=1)  # slower speed and a higher current means more torque.
            self.stepper.home(1)

            return True

        else:
            return False

    def moveToCoordinates(self, desired_x, desired_y, desired_z):
        # move to coordinate position, relative to homed position
        # coordinates are in millimeters
        # is a blocking function, returns when position is reached
        tolerance = 5     # how close the arm must be to the desired coordinates to be considered "there" AKA the window
        
        if self.initialized:
            (angle1, angle2, angle3) = compute_triple_inverse_kinematics(self.homedCoordinates[0] + desired_x, self.homedCoordinates[1] + desired_y, self.homedCoordinates[2] + desired_z)
            pos1 = angle1 * DEG_TO_CPR
            pos2 = angle2 * DEG_TO_CPR
            pos3 = angle3 * DEG_TO_CPR
            self.ax0.set_pos(pos1)
            self.ax1.set_pos(pos2)
            self.ax2.set_pos(pos3)

            # implementation of the old wait function of the stepper motor driver, but now for ODrive
            x_lower = desired_x - tolerance
            x_upper = desired_x + tolerance
            y_lower = desired_y - tolerance
            y_upper = desired_y + tolerance
            z_lower = desired_z - tolerance
            z_upper = desired_z + tolerance
            while True:
                (current_x, current_y, current_z) = self.getHomedCoordinates()
                if (x_lower <= current_x <= x_upper) and (y_lower <= current_y <= y_upper) and (z_lower <= current_z <= z_upper):
                    break

            return

    def moveToRelativeCoordinates(self, offset_x, offset_y, offset_z):
        # move to a position relative to current position
        if self.initialized:
            current_coordinates = self.getHomedCoordinates()
            self.moveToCoordinates(current_coordinates[0] + offset_x, current_coordinates[1] + offset_y, current_coordinates[2] + offset_z)

    def getHomedCoordinates(self):
        # return coordinate position of the end effector, relative to the homed positon
        if self.initialized:
            coordinates = self.getCoordinates()
            corrected_x = coordinates[0] - self.homedCoordinates[0]
            corrected_y = coordinates[1] - self.homedCoordinates[1]
            corrected_z = coordinates[2] - self.homedCoordinates[2]

            return ((corrected_x, corrected_y, corrected_z))

    def getCoordinates(self):
        # return coordinate position of the end effector
        if self.initialized:
            pos1 = self.ax0.get_pos()
            angle1 = pos1 * CPR_TO_DEG

            pos2 = self.ax1.get_pos()
            angle2 = pos2 * CPR_TO_DEG

            pos3 = self.ax2.get_pos()
            angle3 = pos3 * CPR_TO_DEG

            (x, y, z) = forward_kinematics(angle1, angle2, angle3)
            return ((x, y, z))

    def shutdown(self):
        if self.initialized:
            # reset and disconnect from the first ODrive
            try:
                self.od1.reboot()
            except:
                pass

            # reset and disconnect from the second ODrive
            try:
                self.od2.reboot()
            except:
                pass

            # close out of Cyprus and Slush Engine and RPi GPIO
            self.stepper.free_all()
            self.spi.close()
            GPIO.cleanup()
            cyprus.close()

            self.initialized = False
