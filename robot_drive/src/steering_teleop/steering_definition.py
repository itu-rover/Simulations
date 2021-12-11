#!/usr/bin/env python
# -*- coding: utf-8 -*-
import rospy
import sys
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy


class Rover(object):

    def __init__(self):
        rospy.init_node('Steering Rover')
        rospy.Subscriber('/joy', Joy, self.callback)
        self.pub = rospy.Publisher('/four_wheel_steering_controller/cmd_vel', Twist, queue_size=10)
        self.twist = Twist()
        self.angular_axis = 3  # Zero is left analog stick's right and left axes
        self.linear_axis_x = 1  # One is left analog stick's up and down axes
        self.linear_axis_y = 0
        self.lb = 4  # L1 button -> normal mode


        # Keep last angular and linear velocities to publish if no change in axes
        self.last_angular = 0.0
        self.last_linear = 0.0
        self.rate = rospy.Rate(150)
        self.command()

    def callback(self, data):
        if data.buttons[self.lb]:
            self.twist.linear.x = data.axes[self.linear_axis_x] * 0.3
            self.twist.linear.y = data.axes[self.linear_axis_y] * 0.7
            self.twist.angular.z = data.axes[self.angular_axis] * 1

        else: #If RB or LB is not pressed, stop vehicle
            self.twist.linear.x = 0.0
            self.twist.linear.y = 0.0
            self.twist.angular.z = 0.0


    def command(self):
        while not rospy.is_shutdown():
            self.pub.publish(self.twist)
            self.rate.sleep()
            rospy.loginfo("Alt Yurur: \n%s" %self.twist)




def signal_handler(signal_num, frame):
    print(" \n\n\n    GOODBYE :((  \n\n\n   ")
    sys.exit()
