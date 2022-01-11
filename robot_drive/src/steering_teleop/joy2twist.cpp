//ROS
#include "ros/ros.h"
#include "sensor_msgs/Joy.h"
#include "geometry_msgs/Twist.h"
#include "std_msgs/Float64.h"
#include <iostream>
#include <signal.h>

/*
@author: İsmail Eyüphan Ünver
@author: Baran Berk Bağcı
*/

/* This sript written by Han, i just made small changes like ros_info_stream and arm_mode subscriber. */
using namespace std;

bool arm_mode = true;
void mySigintHandler(int sig)
{
  // Do some custom action.
  // For example, publish a stop message to some other nodes.
  
  // All the default sigint handler does is call shutdown()
  ros::shutdown();
}

void joy_cb(const sensor_msgs::Joy::ConstPtr& msg){
  //std_msgs::Bool estop_msg;
  //estop_msg.data = msg->buttons[JOY_BTN_LB] > 0; // Should be 1 or zero
  //estop_pub.publish(estop_msg);

  //btn_dir_data = msg->buttons;
  //ROS_INFO("%d",msg->axes);
  //cout << msg->axes[0]<<endl;
  //joy2twist(msg);
}

void arm_mode_checker(const std_msgs::Float64::ConstPtr& msg) //callback function check /arm_mode topic data 
{
  if (msg->data == 1)
  {
    arm_mode = true;
  }
  else if (msg->data == 0)
  {
    arm_mode = false;
  }
  
  
}
geometry_msgs::Twist twist;


void joy2twist(const sensor_msgs::Joy::ConstPtr& msg){
  twist.angular.z = msg->axes[0]*2*3.1415926535;
  twist.linear.x = msg->axes[4]*10;
  twist.linear.y = msg->axes[3]*10;

  if (!(arm_mode))
  {
    ROS_INFO_STREAM_THROTTLE(0.1,twist);
  }
}

int main(int argc, char **argv)
{

    ros::init(argc, argv, "joy2twist",ros::init_options::NoSigintHandler);
    ros::NodeHandle nh; 
    ros::Publisher twistPub=nh.advertise<geometry_msgs::Twist>("/drive_system/twist", 100);


  ros::Rate rate(150);
  ros::Subscriber joySub = nh.subscribe("/joy", 10, joy2twist);
  ros::Subscriber arm_mod_check = nh.subscribe("/arm_mode", 10, arm_mode_checker);
  
  while (ros::ok)
  {
      ros::spinOnce();
      twistPub.publish(twist);
      rate.sleep();
      signal(1, mySigintHandler);
  }

  //ros::Publisher twistPub = n.advertise<geomerty_msgs::Twist>("chatter", 1000);
  





    return 0;
}


