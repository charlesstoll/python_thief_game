# Vikingbot 0  
# Emma Smith
from time import sleep
import RPi.GPIO as GPIO
global L298N_IN1
global L298N_IN2
global L298N_IN3
global L298N_IN4
global L298N_ENA
global L298N_ENB
global pwm_a
global pwm_b

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

def cleanup():
    GPIO.cleanup()
