
When setting up your encoders there are a number of variables that need to be set on the Odrive

Use the below documentation to determine what variables need to be set to
https://docs.google.com/spreadsheets/d/1OBDwYrBb5zUPZLrhL98ezZbg94tUsZcdTuwiVNgVqpU/edit#gid=0 

FROM ODRIVE:
The following are examples of values that MAY impact the success of calibration. These are not all the varibles you have to set for startup. Only change these when you understand why they are needed; your values will vary depending on your setup:


variables that need to be set
od0.axis0.encoder.config.cpr = 8192 (or some other value)


 od0.axis0.encoder.config.calib_range = 0.05 helps to relax the accuracy of encoder counts during calibration



Testing your encoder:
	od0.axis0.encoder.shadow_count
	




od0.axis0.motor.config.motor_type = MOTOR_TYPE_HIGH_CURRENT select if you have a gimbal or high amp motor
od0.axis0.motor.config.calibration_current = 10.0 sometimes needed if this is a large motor
od0.axis0.motor.config.resistance_calib_max_voltage = 12.0 sometimes needed depending on motor
   
od0.axis0.controller.config.vel_limit = 50000 low values result in the spinning motor stopping abruptly during calibration


FROM ODRIVE:
Tuning the motor controller is an essential step to unlock the full potential of the ODrive. Tuning allows for the controller to quickly respond to disturbances or changes in the system (such as an external force being applied or a change in the setpoint) without becoming unstable. Correctly setting the three tuning parameters (called gains) ensures that ODrive can control your motors in the most effective way possible. The three values are:


    <axis>.controller.config.pos_gain = 20.0 [(counts/s) / counts]
    <axis>.controller.config.vel_gain = 5.0 / 10000.0 [A/(counts/s)]
    <axis>.controller.config.vel_integrator_gain = 10.0 / 10000.0 [A/((counts/s) * s)]



An upcoming feature will enable automatic tuning. Until then, here is a rough tuning procedure:

    Set vel_integrator_gain gain to 0
    Make sure you have a stable system. If it is not, decrease all gains until you have one.
    Increase vel_gain by around 30% per iteration until the motor exhibits some vibration.
    Back down vel_gain to 50% of the vibrating value.
    Increase pos_gain by around 30% per iteration until you see some overshoot.
    Back down pos_gain until you do not have overshoot anymore.
    The integrator can be set to 0.5 * bandwidth * vel_gain, where bandwidth is the overall resulting tracking bandwidth of your system. Say your tuning made it track commands with a settling time of 100ms (the time from when the setpoint changes to when the system arrives at the new setpoint); this means the bandwidth was 1/(100ms) = 1/(0.1s) = 10hz. In this case you should set the vel_integrator_gain = 0.5 * 10 * vel_gain


The liveplotter tool can be immensely helpful in dialing in these values. To display a graph that plots the position setpoint vs the measured position value run the following in the ODrive tool:

start_liveplotter(lambda:[odrv0.axis0.encoder.pos_estimate, odrv0.axis0.controller.pos_setpoint])




