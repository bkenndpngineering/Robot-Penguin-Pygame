# RPi_ODrive
Using RPi with ODrive v3.5 or v3.6 Motor Controller

So you decided to use ODrive, huh? Well well well do I have some info for you.

## Genreal Usage
Plug in the motor and encoder. The order of wires for the motor do not matter in terms of pure functionality. The only thing they change is the direction the motor will move first during encoder calibration. Make sure you use the correct wire order for the encoder though, since the plug order is different for the ODrive board than for other boards we use with the same encoders. Follow the instructions on the front page of the odrive docs (docs.odriverobotics.com). When implementing code into python, run
```python
import odrive
from odrive.enums import *
```
Then you will be able to connect to an ODrive using the command
```python
odrv = odrive.find_any()
```
To connect to multiple odrive boards simultaneously is a little more complicated. The easiest way is to import the ODrive_Ease_Lib file from this repo and run the ```od = ODrive_Ease_Lib.find_ODrives()``` method

The easiest way to control the ODrive is though the ODrive_Ease_Lib Library, since it condenses commonly used commands into singular, short, and intuitive lines. The only major issue with this is that it can send redundant commands. This is not a problem for most situations (where very rapid updates are not required). But in situations like in the Gantry Game or the conference sand table where complex paths are determined by rapidly updating pos_setpoint, the latency can be a problem. The best way of going around this is to just use the native odrive commands where you set the axis requested state and controller control mode a singular time then during updates, only change the pos_setpoint.
It is possible that some of the fields used by ODrive_Ease_Lib are renamed or moved in later versions of the ODrive firmware. This was the case before where the measured velocity from the encoder was previously pll_vel, whereas now it is vel_estimate. 

UNCERTAIN: So it seems that sometimes there are problems when you try to use the ODrive with an RPI right on RPI boot. This can be resolved by throwing a sleep before connecting to the ODrive in scripts that run on system boot. This has worked 5/5 times on the guitar, but no thorough investigation has been done so we aren't sure if this is even really a thing. On the guitar we used a 60 second sleep, but that is probably overkill.

## Calibrating
There are multiple degrees of calibration: none, motor, encoder, complete. Usually, having a calibrated encoder is the same as having a complete calibration. 

A complete calibration sequence can be run by setting an axis' requested state to AXIS_STATE_FULL_CALIBRATION_SEQUENCE. This will run both motor and encoder calibration. This is seen as the motor twitching and making a loud beep then moving slightly to each side before stopping. 

A motor calibration will cause the motor to twitch and then make a beep. You can maintain motor calibration between reboots by setting odrv.axis.motor.config.pre_calibrated to True then running odrv.save_configuration() and odrv.reboot()

An encoder offset calibration must be run after motor calibration. It has the motor move to one side and then the other. If the motor is not able to do this, it will throw an error. While you cannot completely retain encoder calibration between reboots, you can use the encoder index search by following the instructions on the odrive docs.

In ODrive_Ease_Lib, I have a method which accepts a list of ODrive_Axis objects and simultaneously calibrates each of them the minimal amount required. This saves time and energy when dealing with multiple motors.

## Troubleshooting with ODrive!

Format:
hex - dec - meaning - info

Axis errors
0x01 - 1 - invalid state - tried to go into a state you are not allowed to. Usually you tried to do closed loop control before calibrating encoder or tried calibrating encoder before calibrating motor

0x10 - 16 - Break Resistor disarmed. Sometimes the break resistor is disconnected`

0x20, 0x40, 0x60 - 32, 64, 96 - motor not working. Sometimes its a fluke caused by messing around the odrive; fix this by rebooting the odrive. Either that or there is a wire unplugged. Or something whacky is going on that should probably be investigated.

0x100 - 256 - Encoder failure. This can have a number of causes and solutions. Check the encoder error
    Encoder errors
    
    0x02 - 2 - intended CPR not reached. Can be a few issues. Most common is that the motor needs more calibration current. This can be fixed by increasing the calibration current. I think you also need to have the current limit higher than the calibration current but im not certain about this. Next check that the cpr of the encoder is the same as the cpr expected by the odrive. Most of our encoders are 8096 cpr by default but some are 4096. The ODrive expects 8092 by default, so its usually fine. Sometimes wiring issues also cause this problem, but that is uncommon. Its also possible the encoder is kind of broken.

    0x04 - 4 - no signal from encoder. Either the encoder is not corrently wired, or the encoder is broken. Or there is something else but I haven't had this happen yet.

0x200 - 512 - Controller error - Usually the system had an overspeed error. I havent had any other controller errors. Usually overspeed errors aren't a problem so you can fix this by setting the odrv.axis.controller.config.vel_limit_tolerance to 0. This makes it not run the overspeed test. Or you could raise it to a value large enough for it not to matter, but that's only useful where a velocity limit is crucially important.


Other probelms
Sometimes communication to the ODrive cuts out - Yeah thats weird, but it happens. If you are connecting from a device through a USB Hub, sometimes this happens. Try Using a different model USB hub. This happsn often with the type the DPEA has for every surface. Sometimes the problem can be fixed with a reflash of firmware (sent through the ST Link). Also, if you are connecting to a windows computer, sometimes you have to power cycle the ODrive to make it reconnect after a reboot. Windows be whack.

Also if there are different problems, check the ODrive forums/discord. Or if that doesn't work you can send me an email at blakelazarine@dpengineering.org. I will keep notifications on for this email but if I dont reply Mr. Harlow and Mr. Shaeer have my phone number and could send me a text / call me.
By the way, if you get an error but fix it to the point where you think it won't happen again, you can set the errors to 0 (on the axis and on the specific part of the axis (like encoder, motor, controller, etc)). I made a method in ODrive_Ease_Lib which clears the errors, so that's there if you want it. I also have a method for rebooting an ODrive, which can be useful in troubleshooting.

## Hoverboard
The hoverboard motors are best for use in high-precision situations, such as ones where large amounts of power is needed but the range of travel is small, like in the delta arm. There is a hoverboard motor guide on the odrive docs, which is very helpful up until a certain point. The guide encourages use of the hall effect sensor that is built in to the hoverboard motor. This is bad because the hall effect sensor only has 90 cpr and is just overall not as good as using a real encoder. So, you should follow this guide while making sure to leave out the parts dealing with the encoder / hall effect sensor. Some of the encoders we use with the hoverboard motors have 4096 cpr not 8192, so you might have to set the cpr by going into odrv.axis.encoder.config.cpr before calibration. By the way, someitmes when I was running the hoverboard in sensorless mode for extended periods of time, it would get unhappy and throw a motor error. This is weird and I'm not really sure why it happens, but it has been resolved simply by waiting until the next day for it to finish its pout.
Also, the motors only like to work when the motor.config.direction is set to either 1 or -1 (depends on motor I think). Because this value determines the direction of encoder calibration, something you might like to so is set the direction to be, let's say, -1. Then run the encoder index search. Then, once, it's done, immediately set the direction to be 1. This is useful when you are only able to calibrate by moving the motors in a certain direction during calibration/index search.

## Flashing Firmware
There are two primary ways of flashing firmware to the ODrive, instructions for both of which can be found on the odrive tool section of the odrive docs. ODrivetool dfu is done over usb and is useful for updating the firmware on odrive boards that already work perfectly (make sure to use sudo when doing this). The ST Link is used in doing other firmware changes or when dealing with boards that are experiencing firmware issues. We have an ST Link in house with the wires taped in the correct order, which can be found on the odrive docs in case the tape is removed or something changes. For making custom firmware or using the firmware for endstops or something else, you need to compile the firmware files. The ODrive docs have instructions for setting up your device to do this, but they did not work for me without a significant amount of troubleshooting, the exact process of which I do not remember. You should be able to use my old surface (the one labelled Blake Lazarine, its one of the two running linux) to make it work though.

## Using endstops
Github User and ODrive admin Wetmelon made a branch that uses the GPIO pins for endstops. As of right now, it only uses GPIO pins 2 and 8. I found a way of making the other ones work also, but it seemed too easy and obvious so I think it must cause other problems.
In the ODrive Firmware/Board/v3/Src/gpio.c, there is a method header IRQn_Type get_irq_number(uint16_t pin) {. In the large switch statement in this method, there are cases for each GPIO pin. In this statement, the GPIO pin labelled 2 is case 9 (add 7). You can see that only cases 9 and 15 have something assigned to the case.
When you clone the branch, navigate to the Firmware directory and modify the tup.config file, then run ```make```. This will create a build directory. In there will be files ODriveFirmware.elf and ODriveFirmware.hex. I usually use the elf file here but the hex file is also probably fine. In this firmware, if you enable the endstops, it will return an error whenever the endstop is reached, halting the motor's motion. The error can be removed by setting the axis.error to 0 before trying to move again. In ODrive_Ease_Lib I have a method for homing using endstops.

## writing firmware
If you want to make your own firmware, you can just clone the odrive master branch and make modifications. Paul made a branch for deteceting sensor info without forcing a stop.
Generally, you just want to follow the firmware developer guide from the odrive docs.

## Sensorless mode
Sensorless mode is dumb but you need to use it sometimes, like when you are putting the motor into a lathe to center a pin. There is a guide under parameters and commands on the odrive docs, but this does not necessarily work all the time wince sensorless mode is bad. When using a hoverboard motor in sensorless mode, you should be able to just set the axis state and then doing velocity control. Sometimes you have to give the motor a little kick-start, but once it gets going its pretty good. If you are using sensorless mode to turn down a center pin using the lathe, make sure that you have the motor spinning in the correct direction. Sometimes sensorless mode like running in one direction more (less bad sound), which is really strange but if you get it spinning fast everything sort of equals out.

## Using index search
There is one alternative to using the standard encoder offset calibration every time you reboot the ODrive. Instead of having the motor move one way then the other, you can have the motor simply move in one direction until it reaches the encoder index, which remains in the same spot with every reboot.
The ODrive docs have good instructions for using this means of calibration under the encoder page.
With some of the fancier encoder, you can electronically reset the indiex position, but for the standard ones you kind of have to finagle it. You can run the encoder search once to move the encoder into its index position. Then, carefully remove the motor pin from the encoder making sure not to change the encoder position. Then, with the motor separated, rotate the motor to the positionyou want it to end in during calibration. Take into account how gravity will impact rest position while the motor is unpowered. The delta arm uses this system unless I was not able to program it in time.
