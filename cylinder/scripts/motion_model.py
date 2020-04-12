#!/usr/bin/env python3

import rospy
# from gazebo_msgs.srv import GetModelState, GetModelStateResponse
from gazebo_msgs.srv import SetModelState, GetModelState
from gazebo_msgs.msg import ModelState
import numpy as np


# def callback(data):
#     rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
#
# def listener():
#     rospy.init_node('listener', anonymous=True)
#     rospy.Subscriber('/human/get_model_state', ModelState, callback)
#
#     rospy.spin()

class HumanMotion_Gazebo:
    def __init__(self, model_name, motion_model, pmm):
        
        self.motion_model = pmm
        
        self.model_name = model_name
        
        self.x = ModelState()
        
        self.x.model_name = self.model_name
        # self.x.pose.position.x = 0
        # self.x.pose.position.y = 0
        # self.x.pose.position.z = 0
        # self.x.pose.orientation.x = 0
        # self.x.pose.orientation.y = 0
        # self.x.pose.orientation.z = 0
        # self.x.pose.orientation.w = 0
        
    def walk(self, update_rate):
        # t_1 = self.get_clock()
        
        # The rate (Hz) the model updates human states
        rate = rospy.Rate(update_rate)
        delta_t = 1/update_rate
        
        x, y, theta= self.get_human_state()
        
        # self.x.pose.position.x = x + 0.1
        # self.x.pose.position.y = y + 0.1
        # self.set_human_state(self.x)
        
        while not rospy.is_shutdown():
            # Update human states
            x, y, theta = self.motion_model(x, y, theta, delta_t)
            # Update pose msg
            self.x.pose.position.x = x
            self.x.pose.position.y = y
            self.x.pose.orientation.z = theta
            # Ask gazebo to update human state
            self.set_human_state(self.x)
            rate.sleep()
            
        
        
    
    def get_human_state(self):
        rospy.wait_for_service('gazebo/get_model_state')
        
        try:
            get_model_state = rospy.ServiceProxy('gazebo/get_model_state', GetModelState)
            resp1 = get_model_state(self.model_name, 'world')
            
            return resp1.pose.position.x, resp1.pose.position.x, resp1.pose.orientation.z
        except rospy.ServiceException:
            print("Service call failed")
        
        
    def set_human_state(self, x):
        rospy.wait_for_service('gazebo/set_model_state')
        
        try:
            set_model_state = rospy.ServiceProxy('gazebo/set_model_state', SetModelState)
            set_model_state(x)
    #        return resp1.pose
        except rospy.ServiceException:
            print("Service call failed")
            
    def get_clock(self):
        pass

# def get_clock():
#     # Get the simulation clock time
#     pass


class ProbMotionModel:
    def __init__(self, v_mu, v_sigma, theta_dot_mu, theta_dot_sigma, tans_prob):
        self.v_mu = v_mu
        self.v_sigma = v_sigma
        self.theta_dot_mu = theta_dot_mu
        self.theta_dot_sigma = theta_dot_sigma
        self.trans_prob = trans_prob
        
        self.walking = 1
    
    
    def take_one_step(self, x, y, theta, delta_t):
        # Choose if human stops
        self.walking = np.random.choice(1, p=self.trans_prob[self.walking, :])
        if self.walking == 1:
            
            theta_dot = np.random.normal(loc=self.theta_dot_mu, scale=self.theta_dot_sigma)
            theta += theta_dot * delta_t

            v = np.random.normal(loc=self.v_mu, scale=self.v_sigma)
            x += v * np.sin(theta) * delta_t
            y += v * np.cos(theta) * delta_t
            
        return x, y, theta
            
            

if __name__ == '__main__':
    
    # Motion model parameter
    v_mu = 1.47
    v_sigma = 0.12
    theta_dot_mu = 0
    theta_dot_sigma = 0.1
    trans_prob = np.array([[0.5, 0.5], [0.1, 0.9]])
    
    pmm = ProbMotionModel(v_mu, v_sigma, theta_dot_mu, theta_dot_sigma, trans_prob)
    
    hm_gazebo = HumanMotion_Gazebo('cylinder', pmm)
    hm_gazebo.walk(0.5)
    # listener()
    
