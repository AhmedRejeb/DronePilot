#!/usr/bin/env python
""" Drone Pilot - Control of MRUAV """
""" pix-joystick.py -> Script that send the vehicle joystick override using data from a UDP server. """

__author__ = "Aldo Vargas"
__copyright__ = "Copyright 2016 Altax.net"

__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = "Aldo Vargas"
__email__ = "alduxvm@gmail.com"
__status__ = "Development"
__video__ = "http://www.youtube.com/watch?v=TkYeQ6orN8Y"

import sys
sys.path.append("/home/pi/DronePilot/DronePilot/modules/")

import time, threading
from dronekit import connect, VehicleMode
import modules.UDPserver as udp
from modules.utils import *
from modules.pixVehicle import *

# Connection to the vehicle
# SITL via TCP
#vehicle = connect('tcp:127.0.0.1:5760', wait_ready=True)
# SITL/vehicle via UDP (connection coming from mavproxy.py)
#vehicle = connect('udp:127.0.0.1:14549', wait_ready=True)
## Direct UART communication to Pixhawk
vehicle = connect('/dev/serial0', baud=57600, wait_ready=False)  ##MOD 56700

update_rate = 0.01 # 100 hertz update rate
update_rate = 0.5 

vehicle.parameters['ARMING_CHECK']=-9

rcCMD = [1500,1500,1500,1000,1000,1000,1000,1000]
vehicle.channels.overrides = {}  ###+++++++ Ahmed

def sendCommands():
    """
    Function to read commands, modify them and send them. To be called by a thread.
    """
    try:
        while True:
            if udp.active:
                current = time.time()
                elapsed = 0
                # Part for applying commands to the vehicle.
                # Channel order in mavlink:   roll, pitch, throttle, yaw
                # Channel order in optitrack: roll, pitch, yaw, throttle
                #Remember to check min/max for rc channels on APM Planner
                print udp.message ########### ++++++++++++Ahmed
                print "\\\\\\\\\\\\\\\\\\\\\\\\///////////////////////"
                roll     = mapping(udp.message[0],1000,2000,1000,2000)
                pitch    = mapping(udp.message[1],1000,2000,1900,1100) # To invert channel
                throttle = mapping(udp.message[3],1000,2000,986,1998) # Map it to match RC configuration
                yaw      = mapping(udp.message[2],1000,2000,986,1900) # Map it to match RC configuration

                vehicle.channels.overrides = { "1" : roll, "2" : pitch, "3" : throttle, "4" : yaw }
                vehicle.flush()
                time.sleep(0.1)
                print "%s" % vehicle.attitude
                print "Channel overrides 1: %s" % vehicle.channels
                # hz loop
                while elapsed < update_rate:
                    elapsed = time.time() - current
                # End of the main loop
    except Exception,error:
        print "Error on sendCommands thread: "+str(error)
        sendCommands()

""" Section that starts the threads """
try:
    vehicleThread = threading.Thread(target=sendCommands)
    vehicleThread.daemon=True
    vehicleThread.start()
    udp.startTwisted()
except Exception,error:
    print "Error on main script thread: "+str(error)
    vehicle.close()
