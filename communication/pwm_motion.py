# Vikingbot 0  
# Emma Smith
from time import sleep
import RPi.GPIO as GPIO
from Adafruit_BNO055 import BNO055
global L298N_IN1
global L298N_IN2
global L298N_IN3
global L298N_IN4
global L298N_ENA
global L298N_ENB
global pwm_a
global pwm_b
bno = BNO055.BNO055(serial_port='/dev/serial0', rst=18)

def setup():
    global L298N_IN1
    global L298N_IN2
    global L298N_IN3
    global L298N_IN4
    global L298N_ENA
    global L298N_ENB
    global pwm_a
    global pwm_b

#switches on the H-bridge
# Note that the gpio mode is BCM so these numbers do not correspond to the pin numbers on the RPi header
    L298N_IN1 = 26
    L298N_IN2 = 19
    L298N_IN3 = 13
    L298N_IN4 = 6
    L298N_ENA = 16
    L298N_ENB = 12

    #initializing GPIO pins to low outputs 
    GPIO.setup(L298N_IN1, GPIO.OUT)
    GPIO.setup(L298N_IN2, GPIO.OUT)
    GPIO.setup(L298N_IN3, GPIO.OUT)
    GPIO.setup(L298N_IN4, GPIO.OUT)
    GPIO.setup(L298N_ENA, GPIO.OUT)
    GPIO.setup(L298N_ENB, GPIO.OUT)
    GPIO.output(L298N_IN1, GPIO.LOW)
    GPIO.output(L298N_IN2, GPIO.LOW)
    GPIO.output(L298N_IN3, GPIO.LOW)
    GPIO.output(L298N_IN4, GPIO.LOW)
    # Set duty cycle to 100%
    pwm_a = GPIO.PWM(L298N_ENA, 500)
    pwm_b = GPIO.PWM(L298N_ENB, 500)

    # Initial pwms
    pwm_a.start(50)
    pwm_b.start(50)


def RobotFWD(time):
    print("got to fwd")
    global L298N_IN1
    global L298N_IN2
    global L298N_IN3
    global L298N_IN4
    global L298N_ENA
    global L298N_ENB

    GPIO.output(L298N_IN1, GPIO.HIGH)
    GPIO.output(L298N_IN2, GPIO.LOW)
    GPIO.output(L298N_IN3, GPIO.HIGH)
    GPIO.output(L298N_IN4, GPIO.LOW)
    sleep(time)
    RobotSTOP()
    print("got to end of fwd")


def RobotRIGHT(time):
    global L298N_IN1
    global L298N_IN2
    global L298N_IN3
    global L298N_IN4
    global L298N_ENA
    global L298N_ENB


    GPIO.output(L298N_IN1, GPIO.LOW)
    GPIO.output(L298N_IN2, GPIO.HIGH)
    GPIO.output(L298N_IN3, GPIO.HIGH)
    GPIO.output(L298N_IN4, GPIO.LOW)
    sleep(time)
    RobotSTOP()


def RobotLEFT(time):
    global L298N_IN1
    global L298N_IN2
    global L298N_IN3
    global L298N_IN4
    global L298N_ENA
    global L298N_ENB


    GPIO.output(L298N_IN1, GPIO.HIGH)
    GPIO.output(L298N_IN2, GPIO.LOW)
    GPIO.output(L298N_IN3, GPIO.LOW)
    GPIO.output(L298N_IN4, GPIO.HIGH)
    sleep(time)
    RobotSTOP()


def RobotBACK(time):
    global L298N_IN1
    global L298N_IN2
    global L298N_IN3
    global L298N_IN4
    global L298N_ENA
    global L298N_ENB

    GPIO.output(L298N_IN1, GPIO.LOW)
    GPIO.output(L298N_IN2, GPIO.HIGH)
    GPIO.output(L298N_IN3, GPIO.LOW)
    GPIO.output(L298N_IN4, GPIO.HIGH)
    sleep(time)
    RobotSTOP()


def RobotSTOP():
    global L298N_IN1
    global L298N_IN2
    global L298N_IN3
    global L298N_IN4
    global L298N_ENA
    global L298N_ENB

    GPIO.output(L298N_IN1, GPIO.LOW)
    GPIO.output(L298N_IN2, GPIO.LOW)
    GPIO.output(L298N_IN3, GPIO.LOW)
    GPIO.output(L298N_IN4, GPIO.LOW)


def command_arbiter(command, time):
    if command is 'w':
        RobotFWD(time)
    elif command is 'a':
        RobotLEFT(time)
    elif command is 'd':
        RobotRIGHT(time)
    elif command is 's':
        RobotBACK(time)
    else:
        return -1


def get_turn_amount(new_direction):   
    heading, roll, pitch = bno.read_euler()
    current_direction = heading

    turn_amount = new_direction -current_direction 
    turn_amount = (turn_amount + 180) % 360 - 180
    return turn_amount


def turn_to_angle(desired_angle):
   turn_amount = get_turn_amount(desired_angle) 
   # If should be turning left
   if turn_amount < 0:
       while turn_amount < -2:
           RobotLEFT(0.01)
           turn_amount = get_turn_amount(float(desired_angle))
   elif turn_amount > 0:
        while turn_amount > 2:
            RobotRIGHT(0.01)
            turn_amount = get_turn_amount(float(desired_angle))


def cleanup():
    GPIO.cleanup()
