# Demo of reading the range and lux from the VL6180x distance sensor and
# printing it every second.
# Author: Tony DiCola
import time
import board
import busio
import adafruit_vl6180x
import adafruit_tca9548a
import math

# Create I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# create TCA9548a object and give it the bus
tca = adafruit_tca9548a.TCA9548A(i2c, 0x73) # 0x70 default address

# Create sensor instance.

# sensor 1 -- motor 1
# sensor 2 -- motor 2
# sensor 3 -- motor 3

sensor_1 = adafruit_vl6180x.VL6180X(tca[6]) # 6, 4, 2
sensor_2 = adafruit_vl6180x.VL6180X(tca[4])
sensor_3 = adafruit_vl6180x.VL6180X(tca[2])


#####
# dont use EWMA in deltaArm.py --> it would require a thread for constant polling??
#####

# experimental EWMA (exponentially weighted average)
class EWMA:
    def __init__(self, a=0.20, initial_value=0):
        self.a = a
        self.previous_value = initial_value

    def update(self, current_value):
        value = (1-self.a)*self.previous_value + self.a*current_value
        self.previous_value = current_value
        return value

# initialize EWMA filters

sensor_1_ewma = EWMA()
sensor_2_ewma = EWMA()
sensor_3_ewma = EWMA()

def get_angle(sensor):
    # get range from sensor
    range_mm = sensor.range
    print('Range: {0}mm'.format(range_mm))

    # horizontal distance from sensor to motor axle in millimeters
    offset = 80             # approximately, need to verify with CAD
    # distance from top of arm to sensor when the arm is horizontal in millimeters
    horizontal_offset = 33 # verified correct

    A_rad = math.atan((range_mm-horizontal_offset)/offset)
    A_deg = math.degrees(A_rad)
    print('Angle: {}deg'.format(A_deg))

    return A_deg


# Main loop prints the range and lux every second:
while True:
    # Read the range in millimeters and print it.
    #range_mm = sensor.range
    #print('Range: {0}mm'.format(range_mm))
    # Read the light, note this requires specifying a gain value:
    # - adafruit_vl6180x.ALS_GAIN_1 = 1x
    # - adafruit_vl6180x.ALS_GAIN_1_25 = 1.25x
    # - adafruit_vl6180x.ALS_GAIN_1_67 = 1.67x
    # - adafruit_vl6180x.ALS_GAIN_2_5 = 2.5x
    # - adafruit_vl6180x.ALS_GAIN_5 = 5x
    # - adafruit_vl6180x.ALS_GAIN_10 = 10x
    # - adafruit_vl6180x.ALS_GAIN_20 = 20x
    # - adafruit_vl6180x.ALS_GAIN_40 = 40x
    #light_lux = sensor.read_lux(adafruit_vl6180x.ALS_GAIN_1)
    #print('Light (1x gain): {0}lux'.format(light_lux))
    # Delay for a second.
    #time.sleep(0.25)


    # Delta arm angle calculations using TOF sensor
    #           x 
    #           x x
    #           x A x
    #   offset  x     x arm
    #           x       x
    #           x         x
    #           xxxxxxxxxxxxx
    #               range

    # horizontal distance from sensor to motor axle in millimeters
    #offset = 60
    # vertical distance measurement taken by sensor
    #range_mm = range_mm
    # distance from top of arm to sensor when the arm is horizontal in millimeters
    #horizontal_offset = 45

    #A_rad = math.atan((range_mm-horizontal_offset)/offset)
    #A_deg = math.degrees(A_rad)
    #print('Angle: {}deg'.format(A_deg))

    angle_1 = get_angle(sensor_1)
    angle_1_filtered = sensor_1_ewma.update(angle_1)
    print("sensor 1:", angle_1)
    print("sensor 1 EWMA:", angle_1_filtered)
    print()
    angle_2 = get_angle(sensor_2)
    angle_2_filtered = sensor_2_ewma.update(angle_2)
    print("sensor 2:", angle_2)
    print("sensor 2 EWMA:", angle_2_filtered)
    print()
    angle_3 = get_angle(sensor_3)
    angle_3_filtered = sensor_3_ewma.update(angle_3)
    print("sensor 3:", angle_3)
    print("sensor 3 EWMA:", angle_3_filtered)
    print()
    print()

    time.sleep(.25)

