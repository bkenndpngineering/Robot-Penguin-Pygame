# Robot-Penguin-Pygame

DPEA Delta Arm Project 2019-2020
Braedan Kennedy (bkenndpngineering)
Joseph Pearlman (Crocaling)
Philip Nordblad (PhilipNordblad)
Nathaniel Getachew (ngetachew)

Branches:
  Master, contains latest stable version of code.
  Testing, contains latest developments. Constant work in progress.
  
Directories:
  assets, contains images used for the gameboard. The visuals to be shown on screen.
  dpea_p2p, contains the files from the dpea_p2p DPEA repository.
  Delta_Testing_Testing, contains the files from the DPEA Delta Arm API (bkenndpngineering/Delta_Arm_Testing).
  
File Descriptions:
  button.py, contains a Button class. Used for creating buttons on the GUI
  client.py, contains the main program to be run on the Raspberry Pi controlling the Delta Arm Hardware. Interacts with the hardware, displays the gameboard to the screen, communicates with the server for commands.
  clientPoll.py, contains the server and client communication protocol classes. Used for sending and recieving data between the client and server.
  grid.py, contains the gameboard class.
  obstacle.py, contains the Obstacle, Goal, and Player object for the gameboard.
  packetType.py, contains the PacketType enum. Used witht clientPoll server and client objects.
  server.py, contains the main program to be run on the Tablet hosting the user interface. Creates a GUI and communicates commands to the client.
  textures.py, contains the loaded images from the assets directory.
  
Dependencies:
  RPi_ODrive (DPEA repository, included in Delta_Testing_Testing)
  pidev
  Slush
  odrive
  RPi.GPIO
  board
  busio
  adafruit_vl6180x
  adafruit_tca9548a
  spidev
  pygame
  
Hardware Description:
  The DPEA Delta Arm project (otherwise known as the Robot Penguin Project) is a Delta style robotic arm. Its purpose is to provide a visual aide to children learning how to program.
  It encourages thinking ahead, planning, and problem solving. 
  The Delta Arm is controlled by three brushless DC motors. These motors are controlled by an ODrive motor controller, which can give these motors position control with the use of encoders.
  During each system restart each individual motor will need to go through a homing routine to find its position relative to the chassis. Step 1) use the TOF sensor to find the position of each arm and determine which to home first, so it does not harm itself in doing so. 
  Step 2) is raise the motor until the index pulse is found. Step 3) raise the motor until the limit switch is activated.
  The penguin game piece or puck has a white painted screw in its base. When placed over the color sensor its orientation can be found by rotating the puck.
  There is a small stepper motor on the end effector. It is controlled by a Slush Engine. There is small proximity sensor used to home the stepper.
  There is a small electromechanical solenoid. It is controlled by a brushed motor controller. It is important to prevent the solenoid from being left powered on for extended periods of time. It is also important to de-magnetize the iron core by rapidly switching polarity of the input terminals with a descending amount of power.
  There is one main powersupply. There is a smaller step down regulator powersupply for lower voltage components.
  There is a battery pack attached to the Raspberry Pi to allow a safe shutdown when power is cut.
  There is a Cyprus FPGA attached to the Raspberry Pi for increased I/O.
  There is a Slush Engine installed.
  There is a brushed motor controller installed.
  There are two ODrive boards installed (with custom limit switch firmware, no longer necessary)
  There are three TOF lidar sensors installed.
  There is an I2C multiplexer board installed to interface with the TOF sensors.
  There is a large HD screen used for displaying the GUI.
  There is a Surface Tablet used for hosting the GUI.
  There is a Raspberry Pi installed for running the Delta Arm hardware.
  
Known Issues / Hints:
  The ODrive is finicky and can fail for many reasons. The most common ones are 1) the encoder cable is flaky 2) the motor encoder index slipped 3) the power supply is flaking and a larger one needs to be substituted back in 4) the motor needs to be re-calibrated.
  Recalibrating the motor may take several attemps and requires that the limbs be detached from the motor.
  See Delta_Testing_Testing/Utility_Scripts for useful debugging tools.
  See Delta_Teting_Testing/Doc for a complete hardware test and a verified working ODrive motor configuration.
  
  Communication protocol has been rewritten for stability however new features have not been tested extensively. Expect problems.
  
  The Delta Arm needs a start-up sequence, involving homing and orienting the game peice.
  Then the gameboard needs to be displayed and recieve commands while Delta Arm moves the game peice.
  When the player wins or loses the game needs to be reset, the GUI needs to reset, and the Delta Arm needs to move the game peice back to its holder.
  Implement a safe shutdown procedure that allows for a clean start up sequence.
  
  The stepper motor may be too weak for its application. Setting an Angle rarely results in the actual angle being reached. Could be due to the gear down system.
  The solenoid may be too weak for its application. Special programming is required to activate it aggressively to release the game peice.
  The powersupply has been through a lot. A replacement is recommended, one with a higher current rating would be ideal. Expect brown outs if current drawn is too high.
  
  Many hardware difficulties have been overcome in the deltaArm API. Continued use is recommended. It has been extensively tested.
  
  Kivy has been replaced by pygame for simplicity. For future reference.
  
