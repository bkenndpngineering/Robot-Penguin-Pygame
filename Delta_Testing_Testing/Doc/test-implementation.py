# minimalistic script to test API functionality
# Braedan Kennedy (Dec 2, 2019) V.2
from deltaArm import DeltaArm
import time

arm = DeltaArm()

print("Running initialization")
if not arm.initialize():
    exit()
print("finished init")

print("rotating stepper")
arm.rotateStepper(180)
print("rotating stepper again")
arm.rotateStepper(-180)

print("solenoid true")
arm.powerSolenoid(True)
time.sleep(2)
print("solenoid false")
arm.powerSolenoid(False)
time.sleep(2)

# kinematic test
print("moving to (0, 0, -150)")
arm.moveToCoordinates(0, 0, -150)
print("get coordinates test:", arm.getHomedCoordinates())
time.sleep(1)
print("moving to (0, 0, -310)")
arm.moveToCoordinates(0, 0, -310)
print("get coordinates test:", arm.getHomedCoordinates())
time.sleep(1)

# relative movement test
print("relative movement test")
arm.moveToRelativeCoordinates(0, 0, 50) # move up ten millimeters
time.sleep(1)
arm.moveToRelativeCoordinates(0, 0, 50) # move up ten millimeters
time.sleep(1)
arm.moveToRelativeCoordinates(0, 0, 50) # move up ten millimeters
time.sleep(1)

# rapid sequential movement test
print("sequential movement test, no delay")
arm.moveToCoordinates(0, 0, -100)
arm.moveToCoordinates(0, 0, -200)
arm.moveToCoordinates(0, 0, -310)

print("shutoff in 5 seconds")
time.sleep(5)
arm.shutdown()
exit()
