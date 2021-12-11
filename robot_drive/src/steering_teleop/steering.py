#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import Float64 as F64
from sensor_msgs.msg import Joy
from steering_definition import *
from geometry_msgs.msg import Twist
import signal
import pyfiglet



if __name__ == "__main__":

    banner = pyfiglet.figlet_format("ITU ROVER STEERING")
    print(banner)
    signal.signal(signal.SIGINT, signal_handler)
    rover = Rover()
    rospy.spin()