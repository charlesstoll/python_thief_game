"""
Script to receive commands to the Raspberry Pi using a socket server

Author: Charles Stoll, Patrick Gmerek
ECE 579
"""
import sys

import socket
import os
import re
import subprocess
import time
from Adafruit_BNO055 import BNO055

global robot_type
global starting_orientation

def main():
    host = ''
    port = 65432

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(5)

    # In degrees, with the 0 degress pointing straight up
    client_input = '' 
    print('Waiting for connection...')

    while True:
        connection, client_address = s.accept()
        print('Connection from ', client_address)
        client_input = connection.recv(20).decode('ascii')
        print('Received {}'.format(client_input))
        client_input = client_input.split(",")
        if client_input:
            move_robot(client_input[0], client_input[1])

            # Send acknowledge signal back to client
            data = b'ack'
            connection.sendall(data)
            client_input = ''
        else:
            print('no data from', client_address)


def get_orientation():
    global starting_orientation

    # Query the real heading
    heading, roll, pitch = bno.read_euler()

    # Return the difference between the current heading and the starting orientation
    return heading - starting_orientation

def correct_for_drift():
    global starting_orientation
    heading, roll, pitch = bno.read_euler()

    print("In correct_for_drift(), we are comparing the current heading {0:0.2F} against the starting orientation {0:0.2F}".
            format(heading, starting_orientation))

    turn_amount = get_turn_amount(float(starting_orientation))
    print("We need to correct for {} degrees".format(turn_amount))
    # If should be turning left
    if turn_amount < 0:
        while turn_amount < -2:
            command_arbiter('qq')
            turn_amount = get_turn_amount(float(starting_orientation))
    elif turn_amount > 0:
        while turn_amount > 2:
            command_arbiter('ee')
            turn_amount = get_turn_amount(float(starting_orientation))



def get_turn_amount(new_direction):   
    heading, roll, pitch = bno.read_euler()
    current_direction = heading

    turn_amount = new_direction -current_direction 
    turn_amount = (turn_amount + 180) % 360 - 180
    return turn_amount

    
    # Arbitrary threshold is set up right now. Need to test the ripple dance cycle to find out
    # how precisely and accurately we can rotate the hexapod

def move_robot(degrees, distance):
    """
    Looks in the current working directory for a text file with the type of robot
    that this script is running on.
    """
    global robot_type

    print ("Robot type is " + robot_type)
    if robot_type == 'hexapod':
        correct_for_drift()
        #send_motion_command(command, hexapod_motions)
    elif robot_type == 'vikingbot0':
        turn_to_angle(degrees)
        # Multiplier tbd
        sleep_time = distance * 1 
        RobotFWD(float(sleep_time))
    elif robot_type == 'vikingbot1':
        turn_to_angle(degrees)
        # Multiplier tbd
        sleep_time = distance * 1
        RobotFWD(float(sleep_time))


def determine_robot_model():
    # Check what kind of robot this script is running on
    robot_type = ''
    with open ('robot_type.txt', 'r') as f:
        robot_type = (f.readline()).rstrip('\n')

    if robot_type == 'hexapod':
        pass
    elif robot_type == 'vikingbot0':
        pass
    elif robot_type == 'vikingbot1':
        pass
    else:
        print("No valid robot type specified. Read \"{}\", which is not a valid robot.".format(robot_type))
        sys.exit(1)

    return robot_type


if __name__ == "__main__":
    # Store the model of the robot this script is running on
    global robot_type
    global starting_orientation
    robot_type = determine_robot_model()

    bno = BNO055.BNO055(serial_port='/dev/serial0', rst=18)
    heading, roll, pitch = bno.read_euler()
    starting_orientation = heading
    print("Starting orientation (virtual North) is {0:0.2F}".format(starting_orientation)) 

    if not bno.begin():
        raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')

    # Import the functions needed for the appropriate robots
    if robot_type == "hexapod":
        sys.path.append("../../Lynxmotion_Hexapod/game")
        sys.path.append("../../Lynxmotion_Hexapod/project_files/robot_drivers")
        from interactive_control import *
        # Setup the globals needed for the hexpod
        setup()
    else:
        from pwm_motion import *
        setup()

    try:
        main()
    except KeyboardInterrupt:
        print("Received keyboard interrupt!")
        if robot_type == 'vikingbot0':
            GPIO.cleanup()
        sys.exit()

