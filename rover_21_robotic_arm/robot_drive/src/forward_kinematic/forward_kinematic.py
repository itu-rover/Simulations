#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import Float64 as F64
from sensor_msgs.msg import Joy
from F_Arm import *
from std_msgs.msg import Float64MultiArray
from geometry_msgs.msg import Twist

""" Bu kod ileri kinamtik sürüş için yapılmıştır yani kolun eklemlerine ayrı ayrı joystick verileri basılmaktadır hiç bir ters kinematik kodu içermemektedir."""
"""Bu Simulasyonlar için ekleme yapılmıştır DS4 kolunda R2 de mod geçişi olur ve Alt Yürüre geçer HERHANGİ BİR OTONOM HARAKET YOKTUR SİMÜLASYONLARIN 
KONTROLCÜ TESTLERİ İÇİN YAZILMIŞTIR BU KOD ve suan çok ham haldedir en yakın zamanda C++ ile yazılmış daha hoş bir kod yazılacaktır."""

arm = F_ARM()
joy_msg = JOY()


#Get joystick data and convert it to velocity data
#data: Joystick push data
def joy_cb(data):
    if data.buttons[lb]:
        twist.linear.x = data.axes[linear_axis] * 1
        twist.angular.z = data.axes[angular_axis] * 1
    elif data.buttons[rb]:
        twist.linear.x = data.axes[linear_axis] *turbo_multiplier
        twist.angular.z = data.axes[angular_axis] *turbo_multiplier
    else: #If RB or LB is not pressed, stop vehicle
        twist.linear.x = 0.0
        twist.angular.z = 0.0
        joy_msg.buttons[7] = data.buttons[7]
    #Publish velocity data non-stop
def joy_callback(data):

    arm.delta_thetas[0] = data.axes[0] * 0.003
    arm.delta_thetas[1] = data.axes[1] * 0.003
    arm.delta_thetas[2] = data.axes[4] * 0.004
    arm.delta_thetas[3] = -data.axes[3] * 0.003
    arm.delta_thetas[4] = -data.axes[7] * 0.003
    arm.delta_thetas[5] = data.axes[6] * 0.06
    joy_msg.buttons[7] = data.buttons[7]

    # Kare parmakları kapamak Daire parmakları açmak
    arm.gripper_delta_thetas[0] = (data.buttons[1] - data.buttons[3]) * 0.003  # right finger 
    arm.gripper_delta_thetas[1] = (-data.buttons[1] + data.buttons[3]) * 0.003 # left finger

    if data.buttons[4] != 0:
        arm.delta_thetas[6] = data.buttons[4] * 0.004

    else:
        arm.delta_thetas[6] = -data.buttons[5] * 0.004


if __name__ == "__main__":
    rospy.init_node('joy_control')
    joint_1_publisher = rospy.Publisher('/rover_arm_joint_1/command', F64, queue_size=10)
    joint_2_publisher = rospy.Publisher('/rover_arm_joint_2/command', F64, queue_size=10)
    joint_3_publisher = rospy.Publisher('/rover_arm_joint_3/command', F64, queue_size=10)
    joint_4_publisher = rospy.Publisher('/rover_arm_joint_4/command', F64, queue_size=10)
    joint_5_publisher = rospy.Publisher('/rover_arm_joint_5/command', F64, queue_size=10)
    joint_6_publisher = rospy.Publisher('/rover_arm_joint_6/command', F64, queue_size=10)
    
    axis_state = rospy.Publisher('/axis_states/send', Float64MultiArray, queue_size=10)
    axis=[0,0,0,0,0,0]

    right_finger_publisher = rospy.Publisher('/rover_arm_right_finger/command', F64, queue_size=10)
    left_finger_publisher = rospy.Publisher('/rover_arm_left_finger/command', F64, queue_size=10)
    rospy.Subscriber('joy', Joy, joy_callback)

    rate = rospy.Rate(150)
    counter = 0

    first_run = True # ilk adım
    second_part = False # R2 için atanan mod switcin değişkeni
    first_stage = False # R2 için atanan mod switcin değişkeni
    #part_switch = False
    m4 = 0 # 4. motorun ileri kinematik için atanan hız değeri
    m5 = 0 # 5. motorun ileri kinematik için atanan hız değeri

    while not rospy.is_shutdown():
        
        #rospy.loginfo_throttle("I am ready")
        if joy_msg.get_buttons(7) == 1 and not first_stage: # R2 tuşuna atanan mod değişim if bloğu
            first_stage = True

        if first_stage and joy_msg.get_buttons(7) == 0:
            
            if second_part:
                second_part = False

            else:
                second_part = True
            
            first_stage = False # buraya kadar
        if not second_part:
            
            rospy.loginfo_throttle(1,"Robot Arm: joint1: %s, joint2: %s, joint3: %s, joint4: %s, joint5: %s, joint6: %s, gripper_left: %s, gripper_right: %s" 
            %(arm.joint_angles[0], arm.joint_angles[1], arm.joint_angles[2], arm.joint_angles[3], arm.joint_angles[4], arm.joint_angles[5], arm.gripper_angles[0], arm.gripper_angles[1]))

            arm.joint_angles[0] += arm.delta_thetas[0]
            arm.joint_angles[1] += arm.delta_thetas[1]
            arm.joint_angles[2] += arm.delta_thetas[2]
            arm.joint_angles[3] += arm.delta_thetas[3]
            arm.joint_angles[4] += arm.delta_thetas[4]
            arm.joint_angles[5] += arm.delta_thetas[5]

            arm.gripper_angles[0] += arm.gripper_delta_thetas[0]
            arm.gripper_angles[1] += arm.gripper_delta_thetas[1]

            joint_1_publisher.publish(arm.joint_angles[0])
            joint_2_publisher.publish(arm.joint_angles[1])
            joint_3_publisher.publish(arm.joint_angles[2])
            joint_4_publisher.publish(arm.joint_angles[3])
            joint_5_publisher.publish(arm.joint_angles[4])
            joint_6_publisher.publish(arm.joint_angles[5])

            right_finger_publisher.publish(arm.gripper_angles[0])
            left_finger_publisher.publish(arm.gripper_angles[1])

            if counter == 50: #Serial'e gönderilen açı verileri.
                axis[0] = arm.joint_angles[0]
                axis[1] = arm.joint_angles[1]
                axis[2] = arm.joint_angles[2]
                axis[3] = arm.joint_angles[3]
                axis[4] = arm.joint_angles[4]
                axis[5] = arm.joint_angles[5]

                message = Float64MultiArray(data=axis)
                axis_state.publish(message)
                counter = 0

            counter += 1

            rate.sleep()

            

        else: #Rover base teleop control L1 standart drive R1 turbo ride and left analog is for driving
            #teleop = TeleopJoy()
            #rate.sleep()
            rospy.Subscriber("/joy", Joy,joy_cb) #Subscribe to joy topic to get joystick data
            pub = rospy.Publisher("/cmd_vel", Twist, queue_size = 10) #Publish velocity data to /cmd_vel topic

            twist = Twist() #Create empty twist

            angular_axis = 0 #Zero is left analog stick's right and left axes
            linear_axis = 1 #One is left analog stick's up and down axes
            rb = 5 #R1 button -> turbo mode
            lb = 4 #L1 button -> normal mode
            turbo_multiplier = 5 #Turbo mode velocity multiplier

            last_angular = 0.0 #Keep last angular and linear velocities to publish if no change in axes
            last_linear = 0.0
            #rate = rospy.Rate(25) #Publish 25 data every second
            while not rospy.is_shutdown() and second_part:
                pub.publish(twist)
                joint_1_publisher.publish(arm.joint_angles[0])
                joint_2_publisher.publish(arm.joint_angles[1])
                joint_3_publisher.publish(arm.joint_angles[2])
                joint_4_publisher.publish(arm.joint_angles[3])
                joint_5_publisher.publish(arm.joint_angles[4])
                joint_6_publisher.publish(arm.joint_angles[5])
                rospy.loginfo_throttle(1,"Alt Yurur: %s" %twist)
                if joy_msg.get_buttons(7) == 1 and not first_stage: # R2 tuşuna atanan mod değişim if bloğu
                
                    first_stage = True

                if first_stage and joy_msg.get_buttons(7) == 0:
                    
                    if second_part:
                        second_part = False

                    else:
                        second_part = True
                    
                    first_stage = False # buraya kadar
                rate.sleep()
