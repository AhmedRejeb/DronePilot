
# Drone Pilot

Autonomous Pilot software that runs on companion computers. 

Main functionalities:

* Communication with flight controllers, including <Pixhawk, PX4, APM >.
* Bridge between a ground station computer and flight controller, this allows to control vehicles from a computer.
* Black box of flight data (save all the data from the flight controller and ground station).
* Position control algorithms. Uses data from a motion capture system and compute the pilot commands to keep the vehicle in a desired position.
* Uses DroneKit (when using Pixhawk and PX4) to perform advanced missions.
