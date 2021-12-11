#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import math
import rospy 
from std_msgs.msg import Float64 as F64

#global TOLERANCE

#TOLERANCE = 0.001

class F_ARM(object): #ileri kinematik için yazılmıs joint açıları ve değişimlerini tutan class

    def __init__(self):
        self.joint_angles = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.delta_thetas = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        #self.link_lenghts = [26.5, 28.1831, 20.0]
        self.current_pos = [0.0, 0.0, 0.0]
    """
    #İleri kinematikten ters kinematik için düşünülen dönüşüm fonksiyonu.
    def update_position(self):
        theta_1 = self.joint_angles[0]
        theta_2 = self.joint_angles[1] + math.pi/2
        theta_3 = self.joint_angles[2] - math.pi/2
        #self.link_2math.sin(self.theta[0]+self.theta[1])+self.link_1math.sin(self.theta[0])
        z = 27.3 * math.sin(theta_2+theta_3)+ 33.5 * math.sin(theta_2)
        Z = z + 7
        r_vector = 27.3 * math.cos(theta_2+theta_3) + 33.5 * math.cos(theta_2)
        X = r_vector * math.cos(theta_1)
        Y = r_vector * math.sin(theta_1)
        #self.link_2math.cos(self.theta[0]+self.theta[1])+self.link_1math.cos(self.theta[0])
        self.current_pos[0] = X
        self.current_pos[1] = Y
        self.current_pos[2] = Z
        #self.desired_pos = self.current_pos
    """
        


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




"""
class COORDINATS(object):
    def __init__(self, X, Y, Z):
        self.coordinats = [X, Y, Z]

    def get_x(self):
        return self.coordinats[0]

    def get_y(self):
        return self.coordinats[1]
    
    def get_z(self):
        return self.coordinats[2]

"""


            
            
            
            
    

def update_position(theta_1, theta_2, theta_3): #Çalışmayan fonsiyon normalde ileri ile ters kinematik geçişi için ayarlanmış fonksiyonken bu geçiş iptal edildiği için şua anda kullanım dışı
    z = 27.3 * math.sin(theta_2+theta_3)+ 33.5 * math.sin(theta_2)
    z = z + 7
    r_vector = 27.3 * math.cos(theta_2+theta_3) + 33.5 * math.cos(theta_2)
    x = r_vector * math.cos(theta_1)
    y = r_vector * math.sin(theta_1)

    li = [x, y, z]
    return li



def calculate_distance(point1, point2): # noktalar arası uzunluğun hesaplanması
    a = math.pow(point1[0] - point2[0], 2) + math.pow(point1[1] - point2[1], 2) + math.pow(point1[2] - point2[2], 2)

    b = math.sqrt(a)
    return b




def dot_product(point1, point2): # skaler çarpım
    

    result = 0.0

    result += (point1[0] * point2[0]) + (point1[1] * point2[1]) + (point1[2] * point2[2])
    """
    result += point1[1] * point2[1]   #Tek satırda yazmayı dene 
    result += point1[2] * point2[2]
    """
    return result

def angle_of_vectors(point1, point2): # vektörlar arası açının hesaplanması
    
    base_point = [0,0,0]
    
    lenght_of_1 = calculate_distance(point1, base_point)
    lenght_of_2 = calculate_distance(point2, base_point)

    angle = math.acos(dot_product(point1,point2)/(lenght_of_1 * lenght_of_2))* (180/math.pi)

    return angle
       
""" 
Bu fonksiyon rotasyon matrisleri için kullanılmaktadır skaler çarpım sonrası birinci eklemin açısı bulunuduktan sonra diğer eklemleri koordinatların noktasını güncellemekte
"""
def rotate_on_xy(to_be_rotated, angle): 
    radian_angle = angle * math.pi/180

    new_x = (to_be_rotated[0] * math.cos(radian_angle)) - (to_be_rotated[1] * math.sin(radian_angle))
    new_y = (to_be_rotated[0] * math.sin(radian_angle)) + (to_be_rotated[1] * math.cos(radian_angle))       


    to_be_rotated[0] = new_x
    to_be_rotated[1] = new_y

    return to_be_rotated

def crd_multipication(point, factor): # vektörün skalerr bir sayı ile çarpımı sonucu koordinatlarını vermekte fakat orijinal vektörü modifiye etmeden yapmaktadır bunu
    cord = []
    new_x = factor * point[0]
    new_y = factor * point[1]
    new_z = factor * point[2]

    cord.append(new_x)
    cord.append(new_y)
    cord.append(new_z)
    
    return cord

def cosinus_theorem(center, one, two): # kosinüs teoremi
    a = calculate_distance(center, one)
    b = calculate_distance(center, two)
    c = calculate_distance(one, two)

    my_angle = (math.acos((a*a + b*b - c*c)/(2*a*b))*180)/math.pi

    return my_angle

""" 
Bu fonksiyon eklemlerin konumlarına göre açı bulmak için yapılmıştır Bir eklemin açısını bulmak 3 tane eklem gerekmektedir çünkü bu üç eklemden bir üçgen elde ediklecek.
ancak bu açı yanlış bulunabilir çünkü ortak yön olarak 0 pozisyonunda X-Y düzlemine bakan yön seçildi ve bulunan açı bu yöndeki açı değil ise, 360'dan çıkarılması
gerekebilir. Bu durumda vektörel çarpım kullanılır. 3 eklemden orta eklemden bir önceki ekleme giden vektör
A, orta eklemden bir sonraki ekleme giden vektör B ise AxB işleminin sonuç vektörünün Y bileşenine göre (vektörün X bileşeninin işareti
de önemli) açı yönü bulunabilir. 
"""
def find_angle(center, before, nex, joint_1_angle): 
    my_angle = cosinus_theorem(center, before, nex)

    new_before = [before[0] - center[0], before[1] - center[1], before[2] - center[2]]
    new_next = [nex[0] - center[0], nex[1] - center[1], nex[2] - center[2]]

    cross_product_y = (new_before[2] * new_next[0]) - (new_before[0] * new_next[2])

    if ((joint_1_angle < 90) and (joint_1_angle > -90)) and cross_product_y > 0:
        my_angle = 360 - my_angle

    if ((joint_1_angle > 90) or (joint_1_angle < -90)) and cross_product_y < 0:
        my_angle = 360 - my_angle

    return my_angle



"""
FABRIK algoritması psuedo kodun yazıya geçilmiş hali http://andreasaristidou.com/publications/papers/FABRIK.pdf burdan alınmıştır.
my_joints: eklemlerin koordinatlarını verir
link_lenghts: robot kolun uzunluklarını tutan liste.
new_end_point_pos: end efektörün yeni koordinatlarını tutan liste
REACH: Kolun uzanabileciği maksimum boy 

"""
def FABRIK_algorithm(my_joints, link_lenghts, new_end_point_pos, REACH): 
    #global TOLERANCE
    TOLERANCE = 0.1
    i = 0
    r = 0
    lamb = 0
    distance_from_begining = abs(calculate_distance(new_end_point_pos, my_joints[0]))
    
    if distance_from_begining > REACH:
        for i in range(len(my_joints)):
            r = abs(calculate_distance(new_end_point_pos, my_joints[i]))

            lamb = link_lenghts[i]/r
            my_joints[i + 1] = crd_multipication(my_joints[i], 1-lamb) + crd_multipication(new_end_point_pos, lamb)
    
    else:
        b = my_joints[0]
        distance_to_target = calculate_distance(new_end_point_pos, my_joints[len(my_joints) - 1])
        
        while distance_to_target > TOLERANCE:
            my_joints[len(my_joints) - 1] = new_end_point_pos

            for i in range(len(my_joints) - 2, -1, -1):
                r = abs(calculate_distance(my_joints[i + 1], my_joints[i]))
                lamb = link_lenghts[i] / r

                my_joints[i][0] = crd_multipication(my_joints[i+1], 1 - lamb)[0] + crd_multipication(my_joints[i], lamb)[0]
                my_joints[i][1] = crd_multipication(my_joints[i+1], 1 - lamb)[1] + crd_multipication(my_joints[i], lamb)[1]
                my_joints[i][2] = crd_multipication(my_joints[i+1], 1 - lamb)[2] + crd_multipication(my_joints[i], lamb)[2]
                #print(my_joints)
                
            my_joints[0] = b

            for i in range(0,len(my_joints) - 1):
                r = abs(calculate_distance(my_joints[i + 1], my_joints[i]))
                lamb = link_lenghts[i]/ r

                my_joints[i + 1][0] = crd_multipication(my_joints[i], 1 - lamb)[0] + crd_multipication(my_joints[i+1], lamb)[0]
                my_joints[i + 1][1] = crd_multipication(my_joints[i], 1 - lamb)[1] + crd_multipication(my_joints[i+1], lamb)[1]
                my_joints[i + 1][2] = crd_multipication(my_joints[i], 1 - lamb)[2] + crd_multipication(my_joints[i+1], lamb)[2]
            #rospy.loginfo_throttle(2, "--------------------------------------------------")    
            #rospy.loginfo_throttle(2,"Target XF = %s YF = %s ZF = %s" %(new_end_point_pos[0], new_end_point_pos[1], new_end_point_pos[2])) # verilen end effektör konumun Fabrikteki dönüşümünü görmek için eklendi   
            
            distance_to_target = abs(calculate_distance(my_joints[len(my_joints) - 1], new_end_point_pos))

