#!/usr/bin/env python
""" Drone Pilot - Control of MRUAV """
""" pix-takeoff.py -> Script that makes a pixhawk take off in a secure way. DroneKit 2.0 related. """

__author__ = "Aldo Vargas"
__copyright__ = "Copyright 2016 Altax.net"

__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = "Aldo Vargas"
__email__ = "alduxvm@gmail.com"
__status__ = "Development"

import time
from dronekit import connect, VehicleMode
import modules.UDPserver as udp
from modules.utils import *
from modules.pixVehicle import *

# Connection to the vehicle
# SITL via TCP
#vehicle = connect('tcp:127.0.0.1:5760', wait_ready=True)
# SITL/vehicle via UDP (connection coming from mavproxy.py)
#vehicle = connect('udp:127.0.0.1:14550', wait_ready=True)
# Direct UART communication to Pixhawk
#vehicle = connect('/dev/serial0',baud=56700, wait_ready=False)
#+++++++++Ahmed++++
vehicle = connect('/dev/serial0',baud=57600, wait_ready=False)


""" Mission starts here """

print "\n\nAttempting to start take off!!\n\n"
arm_and_takeoff(vehicle, 10)
vehicle.commands.upload() #### add by ahmed
print "Wait 5 seconds before going landing"
print "Current altitude: ", vehicle.location.global_relative_frame.alt
time.sleep(5)
print "\n\nLanding!\n\n"
#vehicle.mode = VehicleMode("RTL")
vehicle.mode = VehicleMode("LAND")
vehicle.commands.upload() #### add by ahmed

while vehicle.armed:
    print "Current altitude: ", vehicle.location.global_relative_frame.alt
    time.sleep(0.5)

print "\n\nMission complete\n\n"
vehicle.close()
