#include <iostream>
#include <signal.h>
#include "ros/ros.h"
#include "geometry_msgs/Twist.h"
#include "sensor_msgs/Joy.h"
#include "trajectory_msgs/JointTrajectory.h"
#include "trajectory_msgs/JointTrajectoryPoint.h"
#include "std_msgs/Float64.h"
#include <ros/console.h>
#include <cmath>
#include <iomanip>

/*
@author: Baran Berk Bağcı
@author: İsmail Eyüphan Ünver
*/

/* 
I made some modifications Han's steering_v2.cpp code this header file written by me however steering class
written by Han.
*/

bool first_stage = false; // This and second_stage variable is used for mode switch algorithm.
bool second_stage = false;

void SigintHandler(int sig) // Han signalHandler function
{
  // Do some custom action.
  // For example, publish a stop message to some other nodes.
  
  // All the default sigint handler does is call shutdown()
  ros::shutdown();
}

class joy_message{ // My Joy class used for gec axis and button value

    double axes[8];
    double buttons[12];


public:
	void set_axes(double,double,double,double,double,double, double, double);
	double get_axis(int);
	void set_buttons(double,double,double,double,double,double,double,double,double,double,double,double);
	double get_button(int);
};

void joy_message::set_axes(double new_axis_0, double new_axis_1, double new_axis_2, double new_axis_3, double new_axis_4, double new_axis_5, double new_axis_6, double new_axis_7){

	axes[0] = new_axis_0;
	axes[1] = new_axis_1;
	axes[2] = new_axis_2;
	axes[3] = new_axis_3;
	axes[4] = new_axis_4;
	axes[5] = new_axis_5;
	axes[6] = new_axis_6;
	axes[7] = new_axis_7;
}



double joy_message::get_axis(int axis_index){

	return axes[axis_index];
}



void joy_message::set_buttons(double new_button_0, double new_button_1, double new_button_2, double new_button_3, double new_button_4, double new_button_5, double new_button_6, double new_button_7, double new_button_8, double new_button_9, double new_button_10, double new_button_11){

	buttons[0] = new_button_0;
	buttons[1] = new_button_1;
	buttons[2] = new_button_2;
	buttons[3] = new_button_3;
	buttons[4] = new_button_4;
	buttons[5] = new_button_5;
	buttons[6] = new_button_6;
	buttons[7] = new_button_7;
	buttons[8] = new_button_8;
	buttons[9] = new_button_9;
	buttons[10] = new_button_10;
	buttons[11] = new_button_11;
}



double joy_message::get_button(int button_index){

	return buttons[button_index];
}

joy_message joy_msg;

class RobotArm // Robot arm class used for drive arm in forward kinematics.
{
private:
	ros::Publisher arm_publisher;
	ros::Publisher right_finger_publisher;
	ros::Publisher left_finger_publisher;
	ros::Subscriber arm_joy;
	//ros::Subscriber arm_mod_switch;
	double arm[6];
	double arm_delta_theta[6];
	double gripper_delta_theta[2];
	double gripper[2];


public:
	RobotArm(ros::NodeHandle *nh){
		arm_publisher = nh->advertise<trajectory_msgs::JointTrajectory>("/rover_arm_controller/command",10); // arm publisher
		ros::Rate rate(150);
		right_finger_publisher = nh->advertise<std_msgs::Float64>("/rover_arm_right_finger/command",10); // right finger gripper publisher
		left_finger_publisher = nh->advertise<std_msgs::Float64>("/rover_arm_left_finger/command",10); // left finger gripper publisher
		arm_joy = nh->subscribe("/joy", 10, &RobotArm::arm_joy_cb,this);

		
		while (ros::ok && !(second_stage)) // while loop for mode switch algorithm
        {
				if ((joy_msg.get_button(7) == 1) && !(first_stage)) // mode switch if block
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
            //std::cout<<"arm"<<std::endl;            
            ros::spinOnce();
            arm_joints(); // main arm drive function
            rate.sleep();
            signal(1, SigintHandler);
            
        }
	}
	// void arm_joy_mod_switch(const sensor_msgs::Joy::ConstPtr& msg)
	// {
	// 	joy_msg.set_buttons(msg->buttons[0],msg->buttons[1],msg->buttons[2],msg->buttons[3],msg->buttons[4],msg->buttons[5],msg->buttons[6],msg->buttons[7],msg->buttons[8],msg->buttons[9],msg->buttons[10],msg->buttons[11]);
    //     //cout << joy_msg.get_button(7)<<endl;
	// }
	void arm_joy_cb(const sensor_msgs::Joy::ConstPtr& msg) // joystck callback for robot arm
	{
		joy_msg.set_axes(msg->axes[0],msg->axes[1],msg->axes[2],msg->axes[3],msg->axes[4],msg->axes[5], msg->axes[6], msg->axes[7]);
		joy_msg.set_buttons(msg->buttons[0],msg->buttons[1],msg->buttons[2],msg->buttons[3],msg->buttons[4],msg->buttons[5],msg->buttons[6],msg->buttons[7],msg->buttons[8],msg->buttons[9],msg->buttons[10],msg->buttons[11]);

	}
	void arm_joints()
	{	
		trajectory_msgs::JointTrajectory arm_msg; // published data to /rover_arm_controller/command topic
		trajectory_msgs::JointTrajectoryPoint arm_point; // attribute of JointTrajectory class it is another class
		arm_msg.joint_names = {"axis_1", "axis_2", "axis_3", "axis_4", "axis_5", "axis_6"}; // joint name for joint trajectory controller.
		
        /* Get all delta theate angle from joystic. */
        arm_delta_theta[0] = joy_msg.get_axis(0) * 0.03;
    	arm_delta_theta[1] = joy_msg.get_axis(1) * 0.03;
   	 	arm_delta_theta[2] = joy_msg.get_axis(4) * 0.04;
    	arm_delta_theta[3] = -joy_msg.get_axis(3) * 0.03;
    	arm_delta_theta[4] = -joy_msg.get_axis(7) * 0.03;
    	arm_delta_theta[5] = joy_msg.get_axis(6) * 0.06;
		gripper_delta_theta[0] = (joy_msg.get_button(1) - joy_msg.get_button(3)) * 0.03;  // right finger 
    	gripper_delta_theta[1] = (-joy_msg.get_button(1) + joy_msg.get_button(3)) * 0.03; // left finger


		for (int i = 0; i < 6; i++)
		{
			arm[i] += arm_delta_theta[i]; /* sum all delta theta to joint angle*/
		}
		
		

		gripper[0] += gripper_delta_theta[0];
        gripper[1] += gripper_delta_theta[1];
		for(double& c: arm) arm_point.positions.push_back(c); /* push point positions to attribute */
		arm_point.time_from_start =ros::Duration(0.005); 
        arm_msg.points.push_back(arm_point); /* points pushed to msg data */
		
		ROS_INFO_STREAM(arm_msg);
        
		arm_publisher.publish(arm_msg); /* msg data published */
		std_msgs::Float64 gripper_pub[2];
		gripper_pub[0].data = gripper[0];
		gripper_pub[1].data = gripper[1];
		right_finger_publisher.publish(gripper_pub[0]);
		left_finger_publisher.publish(gripper_pub[1]);
	}

	~RobotArm()
	{

	}
};

class steering
{
private:
    double Pi = M_PI;


    ros::Publisher pub_steer;
    ros::Publisher pub_wheel[4];
	ros::Publisher arm_mode_pub; //= nh.advertise<std_msgs::Float64>("/arm_mode",10);
    geometry_msgs::Twist twist;
    ros::Subscriber twistSub;
    double _eps = pow(10,-7);
    double zeroPos[4]={Pi/2,Pi/2,Pi/2,Pi/2};
    //double zeroPos[4]={0,0,0,0};

    trajectory_msgs::JointTrajectory steering_msg;
    trajectory_msgs::JointTrajectoryPoint steering_points;

    double steer_arr[4] = {0,0,0,0};
    int    wheel_arr[4] = {0,0,0,0};


public:
    steering(ros::NodeHandle *nh){
        std::cout << std::fixed;
        std::cout << std::setprecision(11);
        pub_steer = nh->advertise<trajectory_msgs::JointTrajectory>("/rover_steering_controller/command",10);
        ros::Rate rate(150);
        pub_wheel[0] = nh->advertise<std_msgs::Float64>("/rover_wheel_leftfront/command" ,10);
        pub_wheel[1] = nh->advertise<std_msgs::Float64>("/rover_wheel_leftrear/command" ,10);
        pub_wheel[2] = nh->advertise<std_msgs::Float64>("/rover_wheel_rightfront/command",10);
        pub_wheel[3] = nh->advertise<std_msgs::Float64>("/rover_wheel_rightrear/command" ,10);
		arm_mode_pub = nh->advertise<std_msgs::Float64>("/arm_mode",10);
		std_msgs::Float64 arm_on;
        arm_on.data = 0.0;
        arm_mode_pub.publish(arm_on);

        pub_steer = nh->advertise<trajectory_msgs::JointTrajectory>("/rover_steering_controller/command",10);


        steering_msg.joint_names= {"steering_leftfront_joint",
                                    "steering_leftrear_joint" ,
                                    "steering_rightrear_joint",
                                    "steering_rightfront_joint"} ; 

      
        twistSub = nh->subscribe("/drive_system/twist",10,&steering::twist_cb,this);
        ros::Subscriber joy_steering_Sub = nh->subscribe("/joy", 10, &steering::steering_joy_cb,this);
        while (ros::ok && second_stage)
        {
                if ((joy_msg.get_button(7) == 1) && !(first_stage))
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
            
            ros::spinOnce();
            action();
            rate.sleep();
            signal(1, SigintHandler);
            
        }
        
    }

    void steering_joy_cb(const sensor_msgs::Joy::ConstPtr& msg){
        joy_msg.set_buttons(msg->buttons[0],msg->buttons[1],msg->buttons[2],msg->buttons[3],msg->buttons[4],msg->buttons[5],msg->buttons[6],msg->buttons[7],msg->buttons[8],msg->buttons[9],msg->buttons[10],msg->buttons[11]);
        //cout << joy_msg.get_button(7)<<endl;
    }
    void twist_cb(const geometry_msgs::Twist& msg){
        twist =msg;
    }

    void tank_rotation(){

        trajectory_msgs::JointTrajectory steering_msg;
        steering_msg.joint_names= {"steering_leftfront_joint",
                                    "steering_leftrear_joint" ,
                                    "steering_rightrear_joint",
                                    "steering_rightfront_joint"} ; 
        trajectory_msgs::JointTrajectoryPoint steering_points;
        for (int i = 0; i < 4; i++) steer_arr[i]= Pi/4 *(((i%2==1)-.5)*2);

        for(double& c: steer_arr) steering_points.positions.push_back(c);
        steering_points.time_from_start =ros::Duration(0.005); 
        steering_msg.points.push_back(steering_points);
        pub_steer.publish(steering_msg);

        std_msgs::Float64 z[4];

        for (int i = 0; i < 4; i++) z[i].data = twist.angular.z*1.7584/2*Pi*(((i>1)-.5)*2);
        for (int i = 0; i < 4; i++) pub_wheel[i].publish(z[i]); 
        
        //cout << twist.angular.z<< endl;
    }

    double stLim(double steer_deg, double dDeg) {
        //cout<<fmod(  steer_deg+dDeg  ,  Pi+_eps)  -Pi/2. << endl;;
        return fmod(  steer_deg+dDeg  ,  Pi+_eps)  -Pi/2. ;}

    void cartesian_wheel_rot(double deg){
        
        trajectory_msgs::JointTrajectory steering_msg;
        steering_msg.joint_names= {"steering_leftfront_joint",
                                    "steering_leftrear_joint" ,
                                    "steering_rightrear_joint",
                                    "steering_rightfront_joint"} ; 
        trajectory_msgs::JointTrajectoryPoint steering_points;

        for (int i = 0; i < 4; i++) steer_arr[i]= stLim(zeroPos[i],deg);
        //cout<< steer_arr[0]<<"  "<< steer_arr[1]<<"  "<< steer_arr[2]<<"  "<< steer_arr[3]<<"  "<<endl;
        for(double& c: steer_arr) steering_points.positions.push_back(c);
        steering_points.time_from_start =ros::Duration(0.005); 
        steering_msg.points.push_back(steering_points);
        pub_steer.publish(steering_msg);

        std_msgs::Float64 z[4];
        for (int i = 0; i < 4; i++) z[i].data = pow(pow(twist.linear.x,2)+pow(twist.linear.y,2),.5)*(((twist.linear.x>=0)-.5)*2);
        for (int i = 0; i < 4; i++) pub_wheel[i].publish(z[i]); 

    }

    void cartesian_motion(){
        double degWheel = atan((twist.linear.y)/(twist.linear.x+_eps));
        if  (isnan(degWheel))  {degWheel=0;} 
        //cout << "vec degree --->  "<<degWheel<<endl;
        cartesian_wheel_rot(degWheel);
    }

    void action(){
        if (twist.angular.z){
            tank_rotation();
        }else{
            cartesian_motion();
        }
    }

    ~steering(){

    }
};

/*
steering::steering()
{
}

steering::~steering()
{
}*/


