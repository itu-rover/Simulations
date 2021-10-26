#!/usr/bin/env python
# -*- coding: utf-8 -*-

import rospy
from std_msgs.msg import Float64 as F64
from sensor_msgs.msg import Joy
from F_Arm import *
from std_msgs.msg import String
import math
from std_msgs.msg import Float64MultiArray

#new_massage = False

#max_reach = 74.6831

joy_msg = JOY()

arm = F_ARM()


global X, Y, Z



    
   

def joy_callback(msg):
    
    global X, Y, Z
    

    X = X + msg.axes[3] * 0.05
    Y = Y + msg.axes[0] * 0.05
    Z = Z + msg.axes[1] * 0.05
    joy_msg.buttons[7] = msg.buttons[7]
    #arm.delta_thetas[0] = msg.axes[0] * 0.05
    #arm.delta_thetas[1] = msg.axes[1] * 0.05
    #arm.delta_thetas[2] = msg.axes[4] * 0.05
    arm.delta_thetas[3] = -msg.axes[4] * 0.004
    arm.delta_thetas[4] = -msg.axes[7] * 0.003
    arm.delta_thetas[5] = msg.axes[6] * 0.006
    
    
    joy_msg.buttons[0] = msg.buttons[4] 
    joy_msg.buttons[1] = msg.buttons[5] 

      
    
    
    
    
    """
    arm.delta_thetas[3] = -msg.axes[3] * 0.003
    arm.delta_thetas[4] = -msg.axes[7] * 0.003
    arm.delta_thetas[5] = msg.axes[6] * 0.006
    """

    


if __name__ == "__main__":
    my_joints = []
    my_joints.append([0.0,0.0,6.0])
    my_joints.append([0.0,0.0,43.5])
    my_joints.append([27.5,0.0,44.5])
    my_joints.append([58.7,0.0,44.5])
    #arm = F_ARM()

    axis=[0,0,0,0,0,0]

    link_lengths = [37.5, 27.5, 31.2]
    REACH = 96.2

    

    rospy.init_node('fabrik')
    joint_1_publisher = rospy.Publisher('/joint__1_controller/command', F64, queue_size=10)
    joint_2_publisher = rospy.Publisher('/joint__2_controller/command', F64, queue_size=10)
    joint_3_publisher = rospy.Publisher('/joint__3_controller/command', F64, queue_size=10)
    joint_4_publisher = rospy.Publisher('/joint__4_controller/command', F64, queue_size=10)
    joint_5_publisher = rospy.Publisher('/joint__5_controller/command', F64, queue_size=10)
    joint_6_publisher = rospy.Publisher('/joint__6_controller/command', F64, queue_size=10)
    axis_state = rospy.Publisher('/axis_states/send', Float64MultiArray, queue_size=10)
    #right_finger_publisher = rospy.Publisher('/rover_arm_right_finger/command', F64, queue_size=10)
    #left_finger_publisher = rospy.Publisher('/rover_arm_left_finger/command', F64, queue_size=10)
    rospy.Subscriber('joy', Joy, joy_callback) 
    

    rate = rospy.Rate(150)

    count = 0
    first_run = True
    second_part = False
    first_stage = False
    part_switch = False
    

    b = False
      
  

    counter = 0 
    
    frst_rn = True

    while not rospy.is_shutdown():
           
        if first_run:
            X = 0
            Y = 0
            Z = 0
            joint_1_angles = 0.0
            first_run = False
        
        

        if joy_msg.get_buttons(7) == 1 and not first_stage:
            first_stage = True

        if first_stage and joy_msg.get_buttons(7) == 0:
            
            if second_part:
                second_part = False

            else:
                second_part = True
            
            first_stage = False
        
        
        if not second_part:
     
            if b:
                theta_1 = arm.joint_angles[0]
                theta_2 = arm.joint_angles[1] + math.pi/2
                theta_3 = arm.joint_angles[2] - math.pi/2
                new_end_point_pos = [0.0, 0.0, 0.0]
                lis = update_position(theta_1, theta_2, theta_3)
                    
                new_end_point_pos[0] = new_end_point_pos[0] + lis[0]  
                new_end_point_pos[1] = new_end_point_pos[1] + lis[1] 
                new_end_point_pos[2] = new_end_point_pos[2] + lis[2]  
                rospy.loginfo_throttle(2,"Target X = %s Y = %s Z= %s" %(new_end_point_pos[0], new_end_point_pos[1], new_end_point_pos[2]))

                rospy.loginfo_throttle(2, "--------------------------------------------------")

                joint_1_angle_differance = (-1.0) * joint_1_angles

                referance_coord_point = [4,0,0]
                proj_joint_1 = [new_end_point_pos[0], new_end_point_pos[1], 0.0]       
                joint_1_angles = angle_of_vectors(proj_joint_1, referance_coord_point)

                if proj_joint_1[1] < 0:
                    joint_1_angles = joint_1_angles * (-1.0)
                    #rosy.loginfo_throttle(2,"Joint_1 angle: %s" %joint_1_angles)
                        
                joint_1_angle_differance += joint_1_angles

                rotate_on_xy(my_joints[0], joint_1_angle_differance)
                rotate_on_xy(my_joints[1], joint_1_angle_differance)
                rotate_on_xy(my_joints[2], joint_1_angle_differance)
                rotate_on_xy(my_joints[3], joint_1_angle_differance)

                FABRIK_algorithm(my_joints, link_lengths, new_end_point_pos, REACH)

                        
                joint_5_angle = find_angle(my_joints[2], my_joints[1], my_joints[3], joint_1_angles)
                joint_3_angle = find_angle(my_joints[1], my_joints[0], my_joints[2], joint_1_angles)
                joint_2_angle = find_angle(my_joints[0], [0.0,0.0,0.0], my_joints[1], joint_1_angles)
                    
                joint_angles = [joint_1_angles, 180.0 - joint_2_angle, 90.0 - (joint_3_angle), 0.0, (joint_5_angle + 180.0) - 270.0]

                joint1_last = (joint_angles[0]*math.pi)/180 
                joint2_last = (joint_angles[1]*math.pi)/180 
                joint3_last = (joint_angles[2]*math.pi)/180 
                joint4_last = (joint_angles[3]*math.pi)/180
                joint5_last = (joint_angles[4]*math.pi)/180
                joint6_last = 0.0
                        
                if counter == 50: 
                    axis[0] = joint1_last
                    axis[1] = joint2_last
                    axis[2] = joint3_last

                    message = Float64MultiArray(data=axis)
                    axis_state.publish(message)
                    counter = 0

                counter += 1 

                rospy.loginfo_throttle(2,"Joint1:%s Joint2:%s Joint3:%s" %(joint1_last, joint2_last, joint3_last))

                    

                        

                joint_1_publisher.publish(joint1_last)
                joint_2_publisher.publish(joint2_last)
                joint_3_publisher.publish(joint3_last)
                #joint_4_publisher.publish(joint4_last)
                #joint_5_publisher.publish(joint5_last)
                #joint_6_publisher.publish(joint6_last)

                arm.joint_angles[0] = joint1_last
                arm.joint_angles[1] = joint2_last
                arm.joint_angles[2] = joint3_last

                rate.sleep()

                p = input("Like to resume inverse kinematics [Y = 1/ N = 0]:")

                if int(p) == 1:
                    b = False

                    
                    

                    
                        
                    


            else:
               
                new_end_point_pos = [58.7,0.0,45.5]
                new_end_point_pos[0] = new_end_point_pos[0] + X  
                new_end_point_pos[1] = new_end_point_pos[1] + Y 
                new_end_point_pos[2] = new_end_point_pos[2] + Z 
                        
                
                            

                    

                rospy.loginfo_throttle(2,"Target X = %s Y = %s Z= %s" %(new_end_point_pos[0], new_end_point_pos[1], new_end_point_pos[2]))

                rospy.loginfo_throttle(2, "--------------------------------------------------")

                joint_1_angle_differance = (-1.0) * joint_1_angles

                referance_coord_point = [4,0,0]
                proj_joint_1 = [new_end_point_pos[0], new_end_point_pos[1], 0.0]       
                joint_1_angles = angle_of_vectors(proj_joint_1, referance_coord_point)

                if proj_joint_1[1] < 0:
                    joint_1_angles = joint_1_angles * (-1.0)
                    #rospy.loginfo_throttle(2,"Joint_1 angle: %s" %joint_1_angles)
                        
                joint_1_angle_differance += joint_1_angles

                rotate_on_xy(my_joints[0], joint_1_angle_differance)
                rotate_on_xy(my_joints[1], joint_1_angle_differance)
                rotate_on_xy(my_joints[2], joint_1_angle_differance)
                rotate_on_xy(my_joints[3], joint_1_angle_differance)

                FABRIK_algorithm(my_joints, link_lengths, new_end_point_pos, REACH)

                        
                joint_5_angle = find_angle(my_joints[2], my_joints[1], my_joints[3], joint_1_angles)
                joint_3_angle = find_angle(my_joints[1], my_joints[0], my_joints[2], joint_1_angles)
                joint_2_angle = find_angle(my_joints[0], [0.0,0.0,0.0], my_joints[1], joint_1_angles)
                if frst_rn:
                    joint_angles = [arm.joint_angles[0], 180 - arm.joint_angles[0], 90.0 - (arm.joint_angles[0]), 0.0, (arm.joint_angles[0] + 180.0) - 270.0]
                    frst_rn = False
                else:       
                    joint_angles = [joint_1_angles, 180 - joint_2_angle, 90.0 - (joint_3_angle), 0.0, (joint_5_angle + 180.0) - 270.0]

                joint1_last = (joint_angles[0]*math.pi)/180 
                joint2_last = (joint_angles[1]*math.pi)/180 
                joint3_last = (joint_angles[2]*math.pi)/180 
                joint4_last = (joint_angles[3]*math.pi)/180
                joint5_last = (joint_angles[4]*math.pi)/180
                joint6_last = 0.0
                        
                

                

                    
                arm.joint_angles[3] += arm.delta_thetas[3]
                arm.joint_angles[4] += arm.delta_thetas[4]
                arm.joint_angles[5] += arm.delta_thetas[5]
                joint4_last = arm.joint_angles[3]
                joint5_last = arm.joint_angles[4]
                joint6_last = arm.joint_angles[5]

                rospy.loginfo_throttle(2,"Joint1:%s Joint2:%s Joint3:%s Joint4:%s Joint5:%s Joint6:%s" %(joint1_last, joint2_last, joint3_last, joint4_last, joint5_last, joint6_last))
                        
                if (joint1_last <= math.pi/4 and joint1_last >= -math.pi/4) or (joint2_last <= 0.01 and joint2_last >= 0.73) or (joint3_last < 0.13 and joint3_last > -0.44):
                    joint_1_publisher.publish(joint1_last)
                    joint_2_publisher.publish(joint2_last)
                    joint_3_publisher.publish(joint3_last)
                    joint_4_publisher.publish(joint4_last)
                    joint_5_publisher.publish(joint5_last)
                    joint_6_publisher.publish(joint6_last)
                    if joy_msg.buttons[0] == 1:
                        joy_msg.buttons[5] = 0
                        joy_msg.buttons[5] = int(joy_msg.buttons[0] * (150))
                        
                    
                    if joy_msg.buttons[1] == 1:
                        joy_msg.buttons[5] = 0
                        joy_msg.buttons[5] = int(joy_msg.buttons[1] * (-150))
                        
                    
                    if counter == 50: 
                        axis[0] = joint1_last
                        axis[1] = joint2_last
                        axis[2] = joint3_last
                        axis[3] = joint4_last
                        axis[4] = joint5_last
                        axis[5] = joy_msg.buttons[5]

                        message = Float64MultiArray(data=axis)
                        axis_state.publish(message)
                        counter = 0

                    counter += 1
                    joy_msg.buttons[5] = 0

                    arm.joint_angles[0] = joint1_last
                    arm.joint_angles[1] = joint2_last
                    arm.joint_angles[2] = joint3_last
                    rate.sleep()

                else:
                    rospy.logerr("Dönüş yok birinci eksende.")
                    pass
                    
                
           
               
               
            
        else:



            rospy.loginfo_throttle(2,"joint1 data is %s" %arm.joint_angles[0])
            rospy.loginfo_throttle(2,"------------------------------------")
            rospy.loginfo_throttle(2,"joint2 data is %s" %arm.joint_angles[1])
            rospy.loginfo_throttle(2,"------------------------------------")
            rospy.loginfo_throttle(2,"joint3 data is %s" %arm.joint_angles[2])
                    
            rospy.loginfo_throttle(2,"------------------------------------")
            rospy.loginfo_throttle(2,"joint4 data is %s" %arm.joint_angles[3])
            rospy.loginfo_throttle(2,"------------------------------------")
            rospy.loginfo_throttle(2,"joint5 data is %s" %arm.joint_angles[4])
            rospy.loginfo_throttle(2,"------------------------------------")
            rospy.loginfo_throttle(2,"joint6 data is %s" %arm.joint_angles[5])
            rospy.loginfo_throttle(2,"------------------------------------")
                    
                    

            arm.joint_angles[0] += arm.delta_thetas[0]
            arm.joint_angles[1] += arm.delta_thetas[1]
            arm.joint_angles[2] += arm.delta_thetas[2]
                    
            arm.joint_angles[3] += arm.delta_thetas[3]
            arm.joint_angles[4] += arm.delta_thetas[4]
            arm.joint_angles[5] += arm.delta_thetas[5]
            """
            joint_1_publisher.publish(arm.joint_angles[0])
            joint_2_publisher.publish(arm.joint_angles[1])
            joint_3_publisher.publish(arm.joint_angles[2])
                    
                    
            if counter == 50: 
                axis[0] = joint1_last
                axis[1] = joint2_last
                axis[2] = joint3_last

                message = Float64MultiArray(data=axis)
                axis_state.publish(message)
                counter = 0

            counter += 1 

            axis[0] = joint1_last
            axis[1] = joint2_last
            axis[2] = joint3_last

            message = Float64MultiArray(data=axis)
            axis_state.publish(message)
            """
            joint_angles = [arm.joint_angles[0], arm.joint_angles[1], arm.joint_angles[2]]
            joint_1_publisher.publish(joint_angles[0])
            joint_2_publisher.publish(joint_angles[1])
            joint_3_publisher.publish(joint_angles[2])
            """
            joint_4_publisher.publish(arm.joint_angles[3])
            joint_5_publisher.publish(arm.joint_angles[4])
            joint_6_publisher.publish(arm.joint_angles[5])
            """

            rate.sleep()        

            b = True
            #print(b)

            
    




