#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import Float64 as F64
from sensor_msgs.msg import Joy
from definitions import *
from geometry_msgs.msg import Twist
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import signal
import pyfiglet

""" Bu kod ileri kinamatik sürüş için yapılmıştır yani kolun eklemlerine ayrı ayrı joystick verileri basılmaktadır hiç bir ters kinematik kodu içermemektedir."""
"""Bu kod robot kolda değişen kontrolcüler için güncellenmiştir ve Jointtrajectory kullanmaktadır ayrıca signal handle ile güzelleşmiştir. En yakın zamanda C++'a geçilecektir."""

if __name__ == "__main__":

    banner = pyfiglet.figlet_format("ITU ROVER TELEOP")

    print(banner)

    rospy.init_node('sim_control')
    arm_publisher = rospy.Publisher('/rover_arm_controller/command', JointTrajectory, queue_size=10) # Arm jointtrajectory publisher publish all joints at the same time
    right_finger_publisher = rospy.Publisher('/rover_arm_right_finger/command', F64, queue_size=10) # Right finger controller
    left_finger_publisher = rospy.Publisher('/rover_arm_left_finger/command', F64, queue_size=10) # Left finger kontroller

    second_part = False  # R2 için atanan mod switcin değişkeni
    first_stage = False  # R2 için atanan mod switcin değişkeni

    signal.signal(signal.SIGINT, signal_handler) # Signal handler print massage when termination signal handled
    
    rate = rospy.Rate(70) # rate value of 150 Hz
    
    while not rospy.is_shutdown():
        if joy_msg.get_buttons(7) == 1 and not first_stage: # R2 tuşuna atanan mod değişim if bloğu
            first_stage = True

        if first_stage and joy_msg.get_buttons(7) == 0:
            
            if second_part:
                second_part = False

            else:
                second_part = True
            
            first_stage = False # buraya kadar

        if not second_part: # Arm Part
            rospy.Subscriber('/joy', Joy, joy_callback)
            rospy.loginfo_throttle(1,"Robot Arm: joint1: %s, joint2: %s, joint3: %s, joint4: %s, joint5: %s, joint6: %s, gripper_left: %s, gripper_right: %s" 
            %(arm.joint_angles[0], arm.joint_angles[1], arm.joint_angles[2], arm.joint_angles[3], arm.joint_angles[4], arm.joint_angles[5], arm.gripper_angles[0], arm.gripper_angles[1])) # Print joint angels

            arm.joint_angles[0] += arm.delta_thetas[0]
            arm.joint_angles[1] += arm.delta_thetas[1]
            arm.joint_angles[2] += arm.delta_thetas[2]
            arm.joint_angles[3] += arm.delta_thetas[3]
            arm.joint_angles[4] += arm.delta_thetas[4]
            arm.joint_angles[5] += arm.delta_thetas[5]

            arm.gripper_angles[0] += arm.gripper_delta_thetas[0]
            arm.gripper_angles[1] += arm.gripper_delta_thetas[1]

            arm_msg = JointTrajectory() # message for joint publisher
            arm_msg.joint_names = ["joint_1", "joint_2", "joint_3", "joint_4", "joint_5", "joint_6"]
            
            arm_points = JointTrajectoryPoint() # contain joint positions
            arm_points.positions = arm.joint_angles
            arm_points.time_from_start = rospy.Duration.from_sec(0.005)

            arm_msg.points.append(arm_points)
            
            arm_publisher.publish(arm_msg) # publish arm positions
            right_finger_publisher.publish(arm.gripper_angles[0]) # Publish Right Finger's position
            left_finger_publisher.publish(arm.gripper_angles[1]) # Publish Left Finger's position
            
            rate.sleep() # sleep in 150 Hz

        else: # Base part
            twist = Twist() # contain twist for rover base
            rospy.Subscriber('/joy', Joy, joy_cb, twist)
            vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size = 10)
            
            while not rospy.is_shutdown() and second_part:
                vel_pub.publish(twist) # publish twist data
                rospy.loginfo_throttle(1,"Alt Yurur: \n%s" %twist)
                if joy_msg.get_buttons(7) == 1 and not first_stage: # R2 tuşuna atanan mod değişim if bloğu
                
                    first_stage = True

                if first_stage and joy_msg.get_buttons(7) == 0:
                    
                    if second_part:
                        second_part = False

                    else:
                        second_part = True
                    
                    first_stage = False # buraya kadar

                rate.sleep() # sleeo in 150 Hz