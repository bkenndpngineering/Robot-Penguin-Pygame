# minimalistic script to test API functionality
# Braedan Kennedy (March 4, 2019) V.3

from deltaArm import DeltaArm
import time

arm = DeltaArm()

# initialize test
print("Running initialization")
if not arm.initialize():
    exit()
print("finished init")

# stepper test
print("stepper test")
print("rotating stepper")
arm.rotateStepper(180)
print("rotating stepper again")
arm.rotateStepper(-180)

# solenoid test
print("solenoid test")
print("solenoid true")
arm.powerSolenoid(True)
time.sleep(2)
print("solenoid false")
arm.powerSolenoid(False)
time.sleep(2)

# kinematic test
print("kinematic test")
print("moving to (0, 0, -50)")
arm.moveToCoordinates(0, 0, -50)
print("get coordinates test:", arm.getHomedCoordinates())
time.sleep(1)
print("moving to (0, 0, -150)")
arm.moveToCoordinates(0, 0, -150)
print("get coordinates test:", arm.getHomedCoordinates())
time.sleep(1)

# relative movement test
print("relative movement test")
arm.moveToRelativeCoordinates(0, 0, 50) # move up
time.sleep(1)
arm.moveToRelativeCoordinates(0, 0, 50) # move up
time.sleep(1)
arm.moveToRelativeCoordinates(0, 0, 50) # move up
time.sleep(1)

# rapid sequential movement test
print("sequential movement test, no delay")
arm.moveToCoordinates(0, 0, -50)
arm.moveToCoordinates(0, 0, -100)
arm.moveToCoordinates(0, 0, -150)

# limit switch polling test
print("limit switch test")
print("lim1: ", arm.getLim1())
print("lim2: ", arm.getLim2())
print("lim3: ", arm.getLim3())

# proximity sensor polling test
print("proximity sensor test")
print("prox: ", arm.getProx())

# TOF sensor polling test
print("TOF sensor test")
print("tof1: ", arm.getTOF1(), " deg")
print("tof2: ", arm.getTOF2(), " deg")
#print("tof3: ", arm.getTOF3(), " deg")

print("shutoff in 5 seconds")
time.sleep(5)
arm.shutdown()
exit()
