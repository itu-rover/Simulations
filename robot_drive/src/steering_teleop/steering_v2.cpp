#include <iostream>
#include <signal.h>
#include "ros/ros.h"
#include "geometry_msgs/Twist.h"
#include "sensor_msgs/Joy.h"
#include "trajectory_msgs/JointTrajectory.h"
#include "trajectory_msgs/JointTrajectoryPoint.h"
#include "std_msgs/Float64.h"
#include <cmath>
#include <iomanip>
#include "definitions.hpp"

/*
@author: Baran Berk Bağcı
@author: İsmail Eyüphan Ünver
*/

/* 
I made some modifications Han's steering_v2.cpp script. 
*/

using namespace std;


void joy_cb(const sensor_msgs::Joy::ConstPtr& msg){ //joystick callback to check mode switch key pressed.
    joy_msg.set_buttons(msg->buttons[0],msg->buttons[1],msg->buttons[2],msg->buttons[3],msg->buttons[4],msg->buttons[5],msg->buttons[6],msg->buttons[7],msg->buttons[8],msg->buttons[9],msg->buttons[10],msg->buttons[11]);
}



int main(int argc, char *argv[])
{
    ros::init(argc, argv, "Steering_system",ros::init_options::NoSigintHandler);
    ros::NodeHandle nh;
    ros::Subscriber joySub = nh.subscribe("/joy", 10, joy_cb);
    ros::Publisher arm_mode_pub = nh.advertise<std_msgs::Float64>("/arm_mode",10);
    while (ros::ok())
    {
        ros::spinOnce(); // this method used for single round callback if you have your own loop this method is usefull.
        if ((joy_msg.get_button(7) == 1) && !(first_stage)) // mode switch algorithm if block 7 button in DS4 is R2 button.
        {
            first_stage = true;
        }
        if ((first_stage) && joy_msg.get_button(7) == 0)
        {
            if (second_stage)
            {
                second_stage = false;
            }

            else
            {
                second_stage = true;
            }
            
            first_stage = false;
            
        }
        
        if (!(second_stage)) // first stage is robot arm control.
        {
            while (ros::ok() && !(second_stage))
            {
                RobotArm arm(&nh);
                std_msgs::Float64 arm_on;
                arm_on.data = 1.0;
                arm_mode_pub.publish(arm_on);
                signal(1, SigintHandler);
            }
            
            
        }
        
        else // second stage is steering control.
        {
            while (ros::ok() && second_stage)
            {
                steering Steering(&nh);
                RobotArm arm(&nh); // do not why necessery but it is essential for keep arm position
                signal(1, SigintHandler);
            }
            

        }
        
        
    }
    
    
    return 0;
}



