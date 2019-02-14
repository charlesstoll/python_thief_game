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
    L298N_IN1 = 37
    L298N_IN2 = 35
    L298N_IN3 = 33
    L298N_IN4 = 31
    L298N_ENA = 36
    L298N_ENB = 32

    GPIO.setmode(GPIO.BOARD)

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
    pwm_a = GPIO.PWM(L298N_ENA, 1000)
    pwm_b = GPIO.PWM(L298N_ENB, 1000)

    # Initial pwms
    pwm_a.start(100)
    pwm_b.start(100)


def RobotFWD():
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
    sleep(.5)
    RobotSTOP()
    print("got to end of fwd")


def RobotRIGHT():
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
    sleep(.2)
    RobotSTOP()


def RobotLEFT():
    print("test L")
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
    sleep(.2)
    RobotSTOP()


def RobotBACK():
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
    sleep(.5)
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


def command_arbiter(command):
    if command is 'w':
        RobotFWD()
    elif command is 'a':
        RobotLEFT()
    elif command is 'd':
        RobotRIGHT()
    elif command is 's':
        RobotBACK()
    else:
        return -1

def cleanup():
    GPIO.cleanup()
