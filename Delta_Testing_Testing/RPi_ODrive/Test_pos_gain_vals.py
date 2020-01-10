import odrive
import time
odrv0 = odrive.find_any()
print(str(odrv0.vbus_voltage))


odrv0.axis0.controller.config.control_mode = 3



for k in range(70, 90):
    print("gain =", k)
    odrv0.axis0.controller.config.pos_gain = k
    start_pos = odrv0.axis0.encoder.pos_estimate

    start_time = time.time()
    odrv0.axis0.controller.pos_setpoint = 50000

    points = []
    while time.time() - start_time < 1.5:
        points.append(odrv0.axis0.encoder.pos_estimate)

    max_diff = 0
    max_idx = 0
    for i in range(len(points)):
        if(abs(points[i]-start_pos) > max_diff):
            max_diff = abs(points[i]-start_pos)
            max_idx = i
    print(points[max_idx])
    print("overshoot by", abs(points[max_idx] - odrv0.axis0.encoder.pos_estimate))
    print('end val', odrv0.axis0.encoder.pos_estimate)
    print('')



    start_pos = odrv0.axis0.encoder.pos_estimate

    start_time = time.time()
    odrv0.axis0.controller.pos_setpoint = 00000

    points = []
    while time.time() - start_time < 1.5:
        points.append(odrv0.axis0.encoder.pos_estimate)

    max_diff = 0
    max_idx = 0
    for i in range(len(points)):
        if(abs(points[i]-start_pos) > max_diff):
            max_diff = abs(points[i]-start_pos)
            max_idx = i
    print(points[max_idx])
    print("overshoot by", abs(points[max_idx] - odrv0.axis0.encoder.pos_estimate))
    print('end val', odrv0.axis0.encoder.pos_estimate)
    print('')

