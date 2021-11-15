#!/usr/bin/env python
# -*- coding: utf-8 -*-


class F_ARM(object):

    def __init__(self):
        self.joint_angles = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.delta_thetas = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.gripper_angles = [0.0, 0.0]
        self.gripper_delta_thetas = [0.0, 0.0, 0.0, 0.0]

class JOY(object): # joy classı tuşları ve axisleri tutuyor ama ana kodda işlevleri oldukça düşük sadece ileri kinematik için hız değerleri için kullanılıyor.

    def __init__(self):
        self.axes = [10.0, 10.0, 10.0, 10.0, 10.0, 0.0]
        self.buttons = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    
    def set_axes(self, new_axis_0, new_axis_1, new_axis_2, new_axis_3, new_axis_4, new_axis_5):
        self.axes[0] = new_axis_0
        self.axes[1] = new_axis_1
        self.axes[2] = new_axis_2
        self.axes[3] = new_axis_3
        self.axes[4] = new_axis_4
        self.axes[5] = new_axis_5

    def get_axes(self,axes_index):
        return self.axes[axes_index]

    def set_buttons(self, new_button_0, new_button_1, new_button_2, new_button_3, new_button_4,  new_button_5,  new_button_6,  new_button_7,  new_button_8,  new_button_9,  new_button_10,  new_button_11):
        self.buttons[0] = new_button_0
        self.buttons[1] = new_button_1
        self.buttons[2] = new_button_2
        self.buttons[3] = new_button_3
        self.buttons[4] = new_button_4
        self.buttons[5] = new_button_5
        self.buttons[6] = new_button_6
        self.buttons[7] = new_button_7
        self.buttons[8] = new_button_8
        self.buttons[9] = new_button_9
        self.buttons[10] = new_button_10
        self.buttons[11] = new_button_11

    def get_buttons(self, buttons_index):
        return self.buttons[buttons_index]