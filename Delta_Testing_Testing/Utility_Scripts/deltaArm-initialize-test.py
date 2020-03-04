from deltaArm import DeltaArm
import time

print("initializing the Delta Arm")
arm = DeltaArm()
arm.initialize()

print("waiting ten seconds")
time.sleep(10)

print("shutting down")
arm.shutdown()
exit()
