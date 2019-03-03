from mpu9250 import mpu9250
from time import sleep
from math import atan2

imu = mpu9250()

while True:
    m = imu.mag
    #print 'Magnet: {:.3f} {:.3f} {:.3f} mT'.format(*m)
    degrees = (atan2(m[1], m[0]) * 180) / 3.14
    print 'Heading in degrees is {:.3f}'.format(degrees)
    sleep(0.5)
