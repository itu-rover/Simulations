#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import Float64MultiArray as F64M
from std_msgs.msg import Float64 as F64
from sensor_msgs.msg import Joy
import signal
import sys

"""
@author: Baran Berk Bağcı
"""

"""This class basicly allow us to drive with forward kinematic drive with velocity controller."""
class Arm(object):
    
    def __init__(self):
        
        rospy.init_node('Arm Velocity Control')
        self.velocities = [0.0, 0.01, 0.01, 0.0, 0.0, 0.0]
        self.gripper_delta_thetas = [0.0, 0.0]
        self.gripper_angles = [0.0, 0.0]
        
        self.arm_publisher = rospy.Publisher('/rover_arm_controller/command', F64M, queue_size=10) #Velocity group controller.
        self.right_finger_publisher = rospy.Publisher('/rover_arm_right_finger/command', F64, queue_size=10) # Right finger controller
        self.left_finger_publisher = rospy.Publisher('/rover_arm_left_finger/command', F64, queue_size=10) # Left finger kontroller
        
        rospy.Subscriber('/joy', Joy, self.joy_callback)

        self.rate = rospy.Rate(150)
        self.arm_velocity_publisher()

    def joy_callback(self, data): #Joy callback
        self.velocities[0] = data.axes[0] * 1
        self.velocities[1] = data.axes[1] * 1
        self.velocities[2] = data.axes[4] * 1
        self.velocities[3] = data.axes[3] * 1
        self.velocities[4] = data.axes[7] * 1
        self.velocities[5] = data.axes[6] * 1
        self.gripper_delta_thetas[0] = (data.buttons[0] - data.buttons[2]) * 0.003  # right finger 
        self.gripper_delta_thetas[1] = (-data.buttons[0] + data.buttons[2]) * 0.003 # left finger

    def arm_velocity_publisher(self):
        while not rospy.is_shutdown():
            message = F64M(data=self.velocities) # Float64MultiArray we need change our float list to Float64MultiArray
            rospy.loginfo_throttle(1,message)
            self.gripper_angles[0] += self.gripper_delta_thetas[0]
            self.gripper_angles[1] += self.gripper_delta_thetas[1]
            self.arm_publisher.publish(message)
            self.right_finger_publisher.publish(self.gripper_angles[0]) # Publish Right Finger's position
            self.left_finger_publisher.publish(self.gripper_angles[1]) # Publish Left Finger's position

            self.rate.sleep() # sleep 150 Hz

def signal_handler(signal_num, frame): #Signal handler when termination accurs print GOODBYE message
    print(" \n\n\n    GOODBYE :((  \n\n\n   ")
    sys.exit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    arm = Arm()