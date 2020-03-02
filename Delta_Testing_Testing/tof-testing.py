# Demo of reading the range and lux from the VL6180x distance sensor and
# printing it every second.
# Author: Tony DiCola
import time
import board
import busio
import adafruit_vl6180x
import math

# Create I2C bus.
i2c = busio.I2C(board.SCL, board.SDA)

# Create sensor instance.
sensor = adafruit_vl6180x.VL6180X(i2c)

# Main loop prints the range and lux every second:
while True:
    # Read the range in millimeters and print it.
    range_mm = sensor.range
    print('Range: {0}mm'.format(range_mm))
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
    offset = 60
    # vertical distance measurement taken by sensor
    range_mm = range_mm
    # distance from top of arm to sensor when the arm is horizontal in millimeters
    horizontal_offset = 45

    A_rad = math.atan((range_mm-horizontal_offset)/offset)
    A_deg = math.degrees(A_rad)
    print('Angle: {}deg'.format(A_deg))
