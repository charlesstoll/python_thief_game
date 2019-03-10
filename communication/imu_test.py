from mpu9250 import mpu9250
from time import sleep
from math import atan2, sqrt, cos, sin
import collections

imu = mpu9250()
BUFF_LEN = 16
yaw_buff = collections.deque(maxlen=BUFF_LEN)

while True:
    a = imu.accel
    g = imu.gyro
    m = imu.mag

    # Get pitch 
    pitch = atan2( a[1], (sqrt( (a[0]*a[0]) + ( a[2] * a[2] ) )))
    # Get roll
    roll = atan2( -a[0], (sqrt((a[1]*a[1]) + (a[2]*a[2]))))
    # Get yaw
    Yh = (m[1] * cos(roll)) - (m[2] * sin(roll))
    Xh = (m[0] * cos(pitch)) + (m[1] * sin(roll) * sin(pitch)) + (m[2] * cos(roll) * sin(pitch))
    yaw = atan2(Yh, Xh)

    print("Pitch angle: %1.3f " % pitch)
    print("Roll angle: %1.3f " % roll)
    print("Yaw angle: %1.3f " % yaw)

    # Apply filtering
    yaw_buff.append(pitch)
    # print(yaw_buff)
    yaw_sum = sum(yaw_buff)
    yaw_val = yaw_sum/BUFF_LEN
    print("Filter Value: %1.3f " % (yaw_val*180/3.141592654))



    #print 'Magnet: {:.3f} {:.3f} {:.3f} mT'.format(*m)

    # m[1] is mag y, m[0] is mag x
    degrees = (atan2(m[1], m[0]) * 180) / 3.1415
    

    #print 'Heading in degrees is {:.3f}'.format(degrees)
    sleep(0.1)
