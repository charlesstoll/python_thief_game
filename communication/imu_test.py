from Adafruit_BNO055 import BNO055
from time import sleep

bno = BNO055.BNO055(serial_port='/dev/serial0', rst=18)

if not bno.begin():
    raise RuntimeError('Failed to initialize BNO055! Is the sensor connected?')


while True:
    # Read the Euler angles for heading, roll, pitch (all in degrees).
    heading, roll, pitch = bno.read_euler()
    # Read the calibration status, 0=uncalibrated and 3=fully calibrated.
    sys, gyro, accel, mag = bno.get_calibration_status()
    # Print everything out.
    print('Heading={0:0.2F}'.format(heading))
    sleep(0.5)
