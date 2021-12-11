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


global X, Y, Z # end effektörün artırılan koordinatları



    
   

def joy_callback(msg):
    
    global X, Y, Z
    

    X = X + msg.axes[3] * (-0.05) # X kooridnatı kontrolcünün sağ analoğunun sağ soludur.
    Y = Y + msg.axes[0] * 0.05 # Y kooridnatı kontrolcünün sol analoğunun sağ soludur.
    Z = Z + msg.axes[1] * 0.05 # Z kooridnatı kontrolcünün sol analoğunun yukarı aşağıdır.
    joy_msg.buttons[7] = msg.buttons[7] # kontrolcünün R2 tuşu
    #joy_msg.buttons[1] = msg.axes[0]   kontrolcünün ileri kinematik için atanan tuşları
    arm.delta_thetas[1] = msg.axes[1] * 0.0025  # ikinci eksen Z kooridnatı kontrolcünün sol analoğunun yukarı aşağıdır.
    joy_msg.buttons[3] = msg.axes[4] 
    #joy_msg.buttons[4] = msg.axes[4] 
    joy_msg.buttons[11] = msg.axes[7] 
    #joy_msg.buttons[6] = msg.axes[6] 

    #arm.delta_thetas[2] = msg.axes[4] * 0.005 simülasyon için  
    arm.delta_thetas[3] = -msg.axes[4] * 0.004 #simülasyon için sağ analog yukarı aşağı
    arm.delta_thetas[4] = -msg.axes[7] * 0.003 #simülasyon için yön tuşları aşağı yukarı
    arm.delta_thetas[5] = msg.axes[6] * 0.006 #simülasyon için yön tuşarı sağ sol
    
    
    joy_msg.buttons[0] = msg.axes[6] #bu iki tuşun simulasyonda karşılığı var artık serialde sonsuz eksen için varlar
    

      
    
    
    
    
    """
    arm.delta_thetas[3] = -msg.axes[3] * 0.003
    arm.delta_thetas[4] = -msg.axes[7] * 0.003
    arm.delta_thetas[5] = msg.axes[6] * 0.006
    """

    


if __name__ == "__main__":
    my_joints = [] # Eklemlerin koordinatlarını tutan liste
    my_joints.append([0.0,0.0,6.0]) # Birinci eksenin koordinatı
    my_joints.append([0.0,0.0,43.5]) # İkinci eksenin koordinatı
    my_joints.append([27.5,0.0,44.5]) # Üçüncü eksenin koordinatı
    my_joints.append([58.7,0.0,44.5]) # End Effector eksenin koordinatı
    #arm = F_ARM()

    axis=[0,0,0,0,0,0] # Seriale gönderilecek açı değerlerini tutan liste.

    link_lengths = [37.5, 27.5, 31.2] # Link uzunluklarını tutan liste.
    REACH = 96.2 # Robot kolun maksimum uzunluğu.

    

    rospy.init_node('fabrik')
    joint_1_publisher = rospy.Publisher('/rover_arm_joint_1/command', F64, queue_size=10) # Controller publisherları
    joint_2_publisher = rospy.Publisher('/rover_arm_joint_2/command', F64, queue_size=10)
    joint_3_publisher = rospy.Publisher('/rover_arm_joint_3/command', F64, queue_size=10)
    joint_4_publisher = rospy.Publisher('/rover_arm_joint_4/command', F64, queue_size=10)
    joint_5_publisher = rospy.Publisher('/rover_arm_joint_5/command', F64, queue_size=10)
    joint_6_publisher = rospy.Publisher('/rover_arm_joint_6/command', F64, queue_size=10)
    axis_state = rospy.Publisher('/axis_states/send', Float64MultiArray, queue_size=10) # Serial koduna verileri gönderen publisher
    #right_finger_publisher = rospy.Publisher('/rover_arm_right_finger/command', F64, queue_size=10)
    #left_finger_publisher = rospy.Publisher('/rover_arm_left_finger/command', F64, queue_size=10)
    rospy.Subscriber('joy', Joy, joy_callback) # Jos subscribe'ı
    

    rate = rospy.Rate(150)

    #count = 0 
    first_run = True # ilk adım
    second_part = False # R2 için atanan mod switcin değişkeni
    first_stage = False # R2 için atanan mod switcin değişkeni
    part_switch = False
    m4 = 0 # 4. motorun ileri kinematik için atanan hız değeri
    m5 = 0 # 5. motorun ileri kinematik için atanan hız değeri

   
      
  

    counter = 0 # Serialin hızını belirleyecek count değeri
    
    frst_rn = True

    while not rospy.is_shutdown():
           
        if first_run: # Bu ilk adımda tüm değerler sıfırlanmıştır
            X = 0
            Y = 0
            Z = 0
            joint_1_angles = 0.0
            first_run = False
        
        
        """ 
        R2 için atanan orijinalde ters ile ileri arası geçiş için düşünülen ancak şimdi işe yaramayan mod geçişi kod bloğu.
        Neden kaldırmadın derseniz ileri ile ters kinematik geçiş çalışmadığı zaman geçişteki kodlar silindi ancak şu anda kod geliştirilmek istenirse 
        diye yedek olarak durmakta bu blok.
        """
        if joy_msg.get_buttons(7) == 1 and not first_stage: # R2 tuşuna atanan mod değişim if bloğu
            first_stage = True

        if first_stage and joy_msg.get_buttons(7) == 0:
            
            if second_part:
                second_part = False

            else:
                second_part = True
            
            first_stage = False # buraya kadar
        
        
        if not second_part:
                
            new_end_point_pos = [58.7,0.0,45.5] # end effektörün konumu
            new_end_point_pos[0] = new_end_point_pos[0] + X  
            new_end_point_pos[1] = new_end_point_pos[1] + Y 
            new_end_point_pos[2] = new_end_point_pos[2] + Z 
                        
                
                            

                    

            rospy.loginfo_throttle(2,"Target X = %s Y = %s Z= %s" %(new_end_point_pos[0], new_end_point_pos[1], new_end_point_pos[2])) #istenilen X Y Z loginfo olarak konsola yazdırılır

            rospy.loginfo_throttle(2, "------------------------------------------------------------------------------------------------------")
            """ Burası birinci ekseni skaler çarpım ile açı farkını buluyor ve robot kolu 2. boyuta indiriyor"""
            joint_1_angle_differance = (-1.0) * joint_1_angles

            referance_coord_point = [4,0,0] # referans vektörü 0. index isteğe bağlı değiştirilebilir
            proj_joint_1 = [new_end_point_pos[0], new_end_point_pos[1], 0.0]       
            joint_1_angles = angle_of_vectors(proj_joint_1, referance_coord_point) # skaler çarpım ile birinci eksenin dönüş açısını belirleyen fonksiyon

            if proj_joint_1[1] < 0: # skaler çarpımın eksi olması durumda açı eksi ile çarpılmakta
                joint_1_angles = joint_1_angles * (-1.0)
                #rospy.loginfo_throttle(2,"Joint_1 angle: %s" %joint_1_angles)
                        
            joint_1_angle_differance += joint_1_angles
            """"""
            rotate_on_xy(my_joints[0], joint_1_angle_differance) #rotasyon matrisleri birinci eksenin dönüşünü referans alarak diğer eklemler hareket ettirmekte
            rotate_on_xy(my_joints[1], joint_1_angle_differance)
            rotate_on_xy(my_joints[2], joint_1_angle_differance)
            rotate_on_xy(my_joints[3], joint_1_angle_differance)

            FABRIK_algorithm(my_joints, link_lengths, new_end_point_pos, REACH) # FABRİK algoritması

            """ 5., 2. ve 3. esksenin açılarının bulunması için gelrekli kodlar """            
            joint_5_angle = find_angle(my_joints[2], my_joints[1], my_joints[3], joint_1_angles)
            joint_3_angle = find_angle(my_joints[1], my_joints[0], my_joints[2], joint_1_angles)
            joint_2_angle = find_angle(my_joints[0], [0.0,0.0,0.0], my_joints[1], joint_1_angles)
            
            if frst_rn: # first runda ilk açılışta seriale hiç tüm açılar sıfır göderiliyor
                joint_angles = [arm.joint_angles[0], 180 - arm.joint_angles[0], 90.0 - (arm.joint_angles[0]), 0.0, (arm.joint_angles[0] + 180.0) - 270.0]
                frst_rn = False
            else: # burda first run bitiyor ve ters kinematik başlıyor       
                joint_angles = [joint_1_angles, 180 - (joint_2_angle), 90.0 - (joint_3_angle ), 0.0, (joint_5_angle + 180.0) - 270.0]

            joint1_last = (joint_angles[0]*math.pi)/180 
            joint2_last = (joint_angles[1]*math.pi)/180  
            joint3_last = (joint_angles[2]*math.pi)/180 
            joint4_last = (joint_angles[3]*math.pi)/180
            joint5_last = (joint_angles[4]*math.pi)/180
            joint6_last = 0.0
                        
                

                

            arm.joint_angles[1] += arm.delta_thetas[1] # ileri kinematik için joystikten alınan açılar toplanıyor   
            arm.joint_angles[3] += arm.delta_thetas[3] # ileri kinematik için joystikten alınan açılar toplanıyor
            arm.joint_angles[4] += arm.delta_thetas[4] # ileri kinematik için joystikten alınan açılar toplanıyor
            arm.joint_angles[5] += arm.delta_thetas[5] # ileri kinematik için joystikten alınan açılar toplanıyor
            joint2_last = arm.joint_angles[1] # normalde ikinci eksen de ters kinematikle ile sürülecekti ancak x ekseni z eksenine çok bağlı olduğu için optimizasyon amacıyla ikinci eksende ileri kinematiğe alınmıştır.
            joint4_last = arm.joint_angles[3] # son 3 eksenin ileri kinematik sürüşü
            joint5_last = arm.joint_angles[4] # son 3 eksenin ileri kinematik sürüşü
            joint6_last = arm.joint_angles[5] # son 3 eksenin ileri kinematik sürüşü
            #rospy.loginfo_throttle(2, "--------------------------------------------------")
            rospy.loginfo_throttle(2,"Joint1:%s Joint2:%s Joint3:%s Joint4:%s Joint5:%s Joint6:%s" %(joint1_last, joint2_last, joint3_last, joint4_last, joint5_last, joint6_last)) #jointlerin açısı info olarak veriliyor print yerine loginfo daha iyi çünkü rahatça periyot ayarlanabiliyor throttle da ilk paramtre periyodu gösterir.
                        
            if (joint1_last <= math.pi/4 and joint1_last >= -math.pi/4) or (joint2_last <= 0.01 and joint2_last >= 0.73) or (joint3_last < 0.13 and joint3_last > -0.44): # sınır değerleri bunlar sağlanmazsa kol sıkışıyor
                """  Bu publisherlar similasyona açıları basmakta """
                joint_1_publisher.publish(joint1_last) 
                joint_2_publisher.publish(joint2_last)
                joint_3_publisher.publish(joint3_last)
                joint_4_publisher.publish(joint4_last)
                joint_5_publisher.publish(joint5_last)
                joint_6_publisher.publish(joint6_last)
                
                if joy_msg.buttons[0] == 1.0: # Sonsuz eksen artı yön sağ taraf
                    joy_msg.buttons[5] = 0
                    joy_msg.buttons[5] = int(joy_msg.buttons[0] * (150))
                        
                    
                if joy_msg.buttons[0] == -1.0: # Sonsuz eksen eksi yön sol taraf
                    joy_msg.buttons[5] = 0
                    joy_msg.buttons[5] = int(joy_msg.buttons[0] * (150))

                if joy_msg.buttons[3] == 1.0: # Dördüncü eksenin ileri kinematik hız değeri artı yön
                    m4 = 0
                    m4 = int(joy_msg.buttons[3] * (150))
                
                if joy_msg.buttons[3] == -1.0: # Dörtüncü eksenin ileri kinematik hız değeri ters yön
                    m4 = 0
                    m4 = int(joy_msg.buttons[3] * (150))

                if joy_msg.buttons[11] == 1.0: # Beşinci eksenin ileri kinematik hız değeri artı yön
                    m5 = 0
                    m5 = int(joy_msg.buttons[11] * (150))

                if joy_msg.buttons[11] == -1.0: # Beşinci eksenin ileri kinematik hız değeri ters yön
                    m5 = 0
                    m5 = int(joy_msg.buttons[11] * (150))
                        
                    
                if counter == 50: #serial mesajı için yapılan if bloğu count elli olduça yayın yapıyor böylece spam önleniyor
                    axis[0] = joint1_last 
                    axis[1] = joint2_last
                    axis[2] = joint3_last
                    axis[3] = m4
                    axis[4] = m5
                    axis[5] = joy_msg.buttons[5]

                    message = Float64MultiArray(data=axis) #seriale e array gönderiliyor
                    axis_state.publish(message)
                    counter = 0
                """ Burda tüm değerler sıfırlanıyor"""
                counter += 1
                joy_msg.buttons[5] = 0
                m4 = 0
                m5 = 0
                arm.joint_angles[0] = joint1_last
                arm.joint_angles[1] = joint2_last
                arm.joint_angles[2] = joint3_last
                rate.sleep()
                """ else bloğu"""
            else:
                rospy.logerr("Out Of Boundries.") # Log error sınırların dışına çıkıldı zaman hata mesjı yayınlar.
                pass
                    
                
           
               
               
            
        else:


            rospy.logwarn("Pass") # Bu mod geçişi işe yaramadığı için warnin mesajı verilir hep.
            pass

            
    




