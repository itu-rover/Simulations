#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys

class ARM(object):

    def __init__(self):
        self.joint_angles = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.delta_thetas = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.gripper_angles = [0.0, 0.0]
        self.gripper_delta_thetas = [0.0, 0.0, 0.0, 0.0]

class JOY(object): # joy classı tuşları ve axisleri tutuyor ama ana kodda işlevleri oldukça düşük sadece ileri kinematik için hız değerleri için kullanılıyor.

    def __init__(self):
        self.axes = [10.0, 10.0, 10.0, 10.0, 10.0, 0.0]
        self.buttons = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    
    def get_buttons(self, buttons_index):
        return self.buttons[buttons_index]

joy_msg = JOY()

"""Callback for rover base"""
def joy_cb(data, twist):
    
    angular_axis = 0 #Zero is left analog stick's right and left axes
    linear_axis = 1 #One is left analog stick's up and down axes
    rb = 5 #R1 button -> turbo mode
    lb = 4 #L1 button -> normal mode
    turbo_multiplier = 5 #Turbo mode velocity multiplier

    last_angular = 0.0 #Keep last angular and linear velocities to publish if no change in axes
    last_linear = 0.0   
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

arm = ARM()

"""Callback for robot arm"""
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

def signal_handler(signal_num, frame):
    print(" \n\n\n    GOODBYE :((  \n\n\n   ")
    sys.exit()