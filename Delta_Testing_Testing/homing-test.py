from deltaArm import DeltaArm
import time

arm = DeltaArm()
arm.initialize()
print("Successfully initialized! Moving arm now")
arm.powerSolenoid(False)
arm.moveToCoordinates(0, 0, -100)
print("Moving Again")
arm.moveToCoordinates(100, 100, -100)
print("shutting down")
time.sleep(3)
arm.shutdown()