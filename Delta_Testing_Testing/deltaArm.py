import os
import spidev
from pidev.stepper import stepper
from pidev.Cyprus_Commands import Cyprus_Commands_RPi as cyprus
from Slush.Devices import L6470Registers
import odrive
from .RPi_ODrive import ODrive_Ease_Lib
import RPi.GPIO as GPIO
from .kinematicFunctions import *
import board
import busio
import adafruit_vl6180x
import adafruit_tca9548a
from .constants import TOF_HORIZONTAL_OFFSET, TOF_VERTICAL_OFFSET, ODRIVE_CONFIG_VARS
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
        self.i2c_initialized = False                # if the i2c bus was not initialized, prevent access to i2c devices

        self.i2c = None
        self.spi = None             # spidev
        self.stepper = None         # stepper motor object
        self.ready = True

        self.ODriveSerialNumber1 = 59877000491063   # first ODrive serial number. Controls motors 1 and 2
        self.ODriveSerialNumber2 = 35623325151307   # second ODrive serial number. Controls motor 3

        self.od1 = None             # first ODrive instance
        self.od2 = None             # second ODrive instance

        self.ax0 = None             # axis 0 of the first ODrive. Motor 1
        self.ax1 = None             # axis 1 of the first ODrive. Motor 2
        self.ax2 = None             # axis 0 of the second ODrive. Motor 3

        self.VL6180X_1 = None       # TOF sensor for Motor 1
        self.VL6180X_2 = None       # TOF sensor for Motor 2
        self.VL6180X_3 = None       # TOF sensor for Motor 3

        self.homedCoordinates = None  # coordinates of the home position, use for relative movement
    
    def rotateStepper(self, degree):
        # rotate stepper motor shaft in degrees
        if self.initialized:
            self.ready = False
            print("step-False")
            preStep = self.stepper.get_position_in_units()
            print(str(preStep))
            Step = 0
            steps = degree * DEG_TO_STEPS
            self.stepper.move_steps(int(steps))
            time.sleep(.8)
            self.ready = True
            print("step-True")

    def powerSolenoid(self, state):
        # Written by Joseph Pearlman and Philip Nordblad
        # toggle solenoid on and off
        if self.initialized:
            cyprus.setup_servo(1)
            if state == True:
                cyprus.set_servo_position(1, 1)
            elif state == False:
                cv = 1
                while cv != .5:
                    cyprus.set_servo_position(1, cv)
                    if cv > .5 and cv - .5 > .009:
                        cv -= .01
                    elif cv < .5 and .5 - cv > .009:
                        cv += .01
                    else:
                        break
                    time.sleep(.01)
                    cv = 1 - cv
                print("demag finished")
                cyprus.set_servo_position(1, .5)
            else:
                print("no valid input")
                return

    def getTOF1(self):
        if self.i2c_initialized:
            # get range from sensor
            range_mm = self.VL6180X_1.range

            A_rad = math.atan((range_mm - TOF_VERTICAL_OFFSET) / TOF_HORIZONTAL_OFFSET)
            A_deg = math.degrees(A_rad)

            return A_deg

    def getTOF2(self):
        if self.i2c_initialized:
            # get range from sensor
            range_mm = self.VL6180X_2.range

            A_rad = math.atan((range_mm - TOF_VERTICAL_OFFSET) / TOF_HORIZONTAL_OFFSET)
            A_deg = math.degrees(A_rad)

            return A_deg

    def getTOF3(self):
        if self.i2c_initialized:
            # get range from sensor
            range_mm = self.VL6180X_3.range

            A_rad = math.atan((range_mm - TOF_VERTICAL_OFFSET) / TOF_HORIZONTAL_OFFSET)
            A_deg = math.degrees(A_rad)

            return A_deg

    def getProx(self):
        if (cyprus.read_gpio() & 0b1000):
            return False
        else:
            return True

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

        # set ODrive parameters
        self.ax2.axis.encoder.config.cpr = ODRIVE_CONFIG_VARS["encoder_cpr"]
        self.ax2.axis.encoder.config.cpr = ODRIVE_CONFIG_VARS["encoder_cpr"]
        self.ax2.axis.encoder.config.cpr = ODRIVE_CONFIG_VARS["encoder_cpr"]

        self.ax2.axis.motor.config.pole_pairs = ODRIVE_CONFIG_VARS["pole_pairs"]
        self.ax1.axis.motor.config.pole_pairs = ODRIVE_CONFIG_VARS["pole_pairs"]
        self.ax0.axis.motor.config.pole_pairs = ODRIVE_CONFIG_VARS["pole_pairs"]

        self.ax2.axis.motor.config.requested_current_range = ODRIVE_CONFIG_VARS["requested_current_range"]
        self.ax1.axis.motor.config.requested_current_range = ODRIVE_CONFIG_VARS["requested_current_range"]
        self.ax0.axis.motor.config.requested_current_range = ODRIVE_CONFIG_VARS["requested_current_range"]

        self.ax2.axis.motor.config.current_control_bandwidth = ODRIVE_CONFIG_VARS["current_control_bandwidth"]
        self.ax1.axis.motor.config.current_control_bandwidth = ODRIVE_CONFIG_VARS["current_control_bandwidth"]
        self.ax0.axis.motor.config.current_control_bandwidth = ODRIVE_CONFIG_VARS["current_control_bandwidth"]

        self.ax2.axis.motor.config.current_lim = ODRIVE_CONFIG_VARS["current_lim"]
        self.ax1.axis.motor.config.current_lim = ODRIVE_CONFIG_VARS["current_lim"]
        self.ax0.axis.motor.config.current_lim = ODRIVE_CONFIG_VARS["current_lim"]

        self.ax2.axis.motor.config.calibration_current = ODRIVE_CONFIG_VARS["calibration_current"]
        self.ax1.axis.motor.config.calibration_current = ODRIVE_CONFIG_VARS["calibration_current"]
        self.ax0.axis.motor.config.calibration_current = ODRIVE_CONFIG_VARS["calibration_current"]

        self.ax2.axis.controller.config.vel_integrator_gain = ODRIVE_CONFIG_VARS["vel_integrator_gain"]
        self.ax1.axis.controller.config.vel_integrator_gain = ODRIVE_CONFIG_VARS["vel_integrator_gain"]
        self.ax0.axis.controller.config.vel_integrator_gain = ODRIVE_CONFIG_VARS["vel_integrator_gain"]

        self.ax2.axis.controller.config.vel_gain = ODRIVE_CONFIG_VARS["vel_gain"]
        self.ax1.axis.controller.config.vel_gain = ODRIVE_CONFIG_VARS["vel_gain"]
        self.ax0.axis.controller.config.vel_gain = ODRIVE_CONFIG_VARS["vel_gain"]

        self.ax2.axis.controller.config.pos_gain = ODRIVE_CONFIG_VARS["pos_gain"]
        self.ax1.axis.controller.config.pos_gain = ODRIVE_CONFIG_VARS["pos_gain"]
        self.ax0.axis.controller.config.pos_gain = ODRIVE_CONFIG_VARS["pos_gain"]
        
        return True

    def homeMotors(self):
        # move the motors to index position. Requirement for position control
        if self.ax2.is_calibrated():
            print("self.ax1.is_calibrated()")
            self.ax2.index_and_hold(-1, 1)
            print('self.ax2.index_and_hold(-1, 1)')
            time.sleep(1)
            self.ax0.index_and_hold(-1, 1)
            print('self.ax0.index_and_hold(-1, 1)')
            time.sleep(1)
            self.ax1.index_and_hold(-1, 1)
            print('self.ax1.index_and_hold(-1, 1)')
            time.sleep(1)
        else:
            print("ax1 not calibrated")

        # home motor 3
        self.ax2.set_vel(-20)
        print("set ax2 vel")
        while (not self.getLim3()):
            continue
        print("getLim3")
        self.ax2.set_vel(0)
        self.ax2.set_home()
        print("set ax2 home")
        time.sleep(1)

        # home motor 1
        self.ax0.set_vel(-20)
        print("set ax0 vel")
        while (not self.getLim1()):
            continue
        print("getLim1")
        self.ax0.set_vel(0)
        self.ax0.set_home()
        print("set ax2 home")
        time.sleep(1)

        # home motor 2
        self.ax1.set_vel(-20)
        print("set ax1 vel")
        while (not self.getLim2()):
            continue
        print("getLim2")
        self.ax1.set_vel(0)
        self.ax1.set_home()
        print("set ax2 home")
        time.sleep(1)

        # if anything is wrong with ODrive, the homing sequence will be registered as a failure

        if self.ax2.axis.error != 0:
            print("ax2.axis failure" + str(self.ax2.axis.error))
            print("ax2.axis.motor failure" + str(self.ax2.axis.motor.error))
            print("ax2.axis.encoder failure" + str(self.ax2.axis.encoder.error))
            print("ax2.axis.controller failure" + str(self.ax2.axis.controller.error))
            return False
        if self.ax2.axis.motor.error != 0:
            return False
        if self.ax2.axis.encoder.error != 0:
            return False
        if self.ax2.axis.controller.error != 0:
            return False

        if self.ax0.axis.error != 0:
            print("ax0.axis failure" + str(self.ax0.axis.error))
            print("ax0.axis.motor failure" + str(self.ax0.axis.motor.error))
            print("ax0.axis.encoder failure" + str(self.ax0.axis.encoder.error))
            print("ax0.axis.controller failure" + str(self.ax0.axis.controller.error))
            return False
        if self.ax0.axis.motor.error != 0:
            return False
        if self.ax0.axis.encoder.error != 0:
            return False
        if self.ax0.axis.controller.error != 0:
            return False

        if self.ax1.axis.error != 0:
            print("ax1.axis failure" + str(self.ax1.axis.error))
            print("ax1.axis.motor failure" + str(self.ax1.axis.motor.error))
            print("ax1.axis.encoder failure" + str(self.ax1.axis.encoder.error))
            print("ax1.axis.controller failure" + str(self.ax1.axis.controller.error))
            return False
        if self.ax1.axis.motor.error != 0:
            return False
        if self.ax1.axis.encoder.error != 0:
            return False
        if self.ax1.axis.controller.error != 0:
            return False

        return True

    def initialize(self):
        # returns true is successful, false if not

        print("Initialize I2C bus")
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.TCA9548a = adafruit_tca9548a.TCA9548A(i2c)
        self.VL6180X_1 = adafruit_vl6180x.VL6180X(self.TCA9548a[6])
        self.VL6180X_2 = adafruit_vl6180x.VL6180X(self.TCA9548a[4])
        #self.VL6180X_3 = adafruit_vl6180x.VL6180X(self.TCA9548a[6])
        print("Initialized I2C objects")
        self.i2c_initialized = True

        # setup limit switches and solenoid
        self.spi = spidev.SpiDev()
        cyprus.initialize()
        version = cyprus.read_firmware_version()
        print("Found CyPrus, Firmware version: ", version)

        # connect to ODrives
        print('ODriveConnected = self.connectODrive()')
        ODriveConnected = self.connectODrive()

        if (ODriveConnected == True):
            # if GPIO and ODrive are setup properly, attempt to home
            print('HomedMotors = self.homeMotors()')
            HomedMotors = self.homeMotors()
            print(HomedMotors)
            if (HomedMotors == True):
                self.initialized = True
                print("initialized")
            else:
                print("Home Failure")

        if self.initialized:
            # calculate homed coordinates
            self.homedCoordinates = self.getCoordinates()

            # setup and home stepper
            self.stepper = stepper(port=0, micro_steps=32, hold_current=40, run_current=40, accel_current=40,
                                   deaccel_current=40, steps_per_unit=200,
                                   speed=1)  # slower speed and a higher current means more torque.
            self.stepper.home(1)
            print("initialize True")
            return True

        else:
            return False

    def moveToCoordinates(self, desired_x, desired_y, desired_z):
        # move to coordinate position, relative to homed position
        # coordinates are in millimeters
        # is a blocking function, returns when position is reached
        tolerance = 4    # how close the arm must be to the desired coordinates to be considered "there" AKA the window
        while not self.ready:
            pass
        if self.initialized:
       
            current_x, current_y, current_z = self.getCoordinates()
            """ if desired_x > current_x:
                desired_x += tolerance*2
            else:
                desired_x -= tolerance*2
            if desired_y < current_y:
                desired_y += tolerance*2
            else:
                desired_y -= tolerance*2
            if desired_z > current_z:
                desired_z += tolerance
            else:
                desired_z -= tolerance
            """
            (angle1, angle2, angle3) = compute_triple_inverse_kinematics(self.homedCoordinates[0] + desired_x, self.homedCoordinates[1] + desired_y, self.homedCoordinates[2] + desired_z)
            pos1 = angle1 * DEG_TO_CPR
            pos2 = angle2 * ABS_DEG_TO_CPR
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
            print("Desired:")
            print(desired_x, desired_y, desired_z)
            while True:
                (current_x, current_y, current_z) = self.getHomedCoordinates()
                if (x_lower <= current_x <= x_upper) and (y_lower <= current_y <= y_upper) and (z_lower <= current_z <= z_upper):
                    print("Actual:")
                    print(current_x, current_y, current_z)
                    break
                else:
                    print(current_x, current_y, current_z)

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
            angle2 = pos2 * ABS_CPR_TO_DEG


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
