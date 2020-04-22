#!/usr/bin/env python3
"""
Human motion control ros node

Jing Huang

Subscribe:
    'gazebo/get_model_state'



"""

import rospy
# from gazebo_msgs.srv import GetModelState, GetModelStateResponse
from gazebo_msgs.srv import SetModelState, GetModelState
from gazebo_msgs.msg import ModelState
import numpy as np


class HumanMotion_Gazebo:
    def __init__(self, model_name, motion_model):

        self.motion_model = motion_model

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

        self.info = ['STOP', 'WALK']

    def walk(self, update_rate):
        # t_1 = self.get_clock()

        # The rate (Hz) the model updates human states
        rospy.init_node('human_control', anonymous=True)
        rate = rospy.Rate(update_rate)
        delta_t = 1/update_rate

        position, orientation = self.get_human_state()

        self.x.pose.orientation = orientation

        x = position.x
        y = position.y
        theta = 0
        # self.x.pose.position.x = x + 0.1
        # self.x.pose.position.y = y + 0.1
        # self.set_human_state(self.x)

        while not rospy.is_shutdown():
            # Update human states
            x, y, theta = self.motion_model.take_one_step(x, y, theta, delta_t)
            # Update pose msg
            self.x.pose.position.x = x
            self.x.pose.position.y = y
            # self.x.pose.orientation.z = theta
            # Ask gazebo to update human state
            self.set_human_state(self.x)

            print("[%s] Human position: x=%g, y=%g, theta=%g"\
             %(self.info[self.motion_model.walking], x, y, theta))
            # print(self.x)

            rate.sleep()


    def get_human_state(self):
        rospy.wait_for_service('gazebo/get_model_state')

        try:
            get_model_state = rospy.ServiceProxy('gazebo/get_model_state', GetModelState)
            resp1 = get_model_state(self.model_name, 'world')
            # print(resp1)
            return resp1.pose.position, resp1.pose.orientation
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

class ProbMotionModel:
    def __init__(self, v_mu, v_sigma, theta_dot_mu, theta_dot_sigma, trans_prob):
        self.v_mu = v_mu
        self.v_sigma = v_sigma
        self.theta_dot_mu = theta_dot_mu
        self.theta_dot_sigma = theta_dot_sigma
        self.trans_prob = trans_prob

        self.walking = 1


    def take_one_step(self, x, y, theta, delta_t):
        # Choose if human stops
        self.walking = np.random.choice([0, 1], p=self.trans_prob[self.walking, :])
        if self.walking == 1:

            theta_dot = np.random.normal(loc=self.theta_dot_mu, scale=self.theta_dot_sigma)
            theta += theta_dot * delta_t

            v = np.random.normal(loc=self.v_mu, scale=self.v_sigma)
            x += v * np.cos(theta) * delta_t
            y += v * np.sin(theta) * delta_t

        return x, y, theta



if __name__ == '__main__':

    # Motion model parameter
    rate = 5

    v_mu = 0.5/rate
    v_sigma = 0.012/rate
    theta_dot_mu = 0
    theta_dot_sigma = 0.2/rate
    trans_prob = np.array([[0.3, 0.7], [0.01, 0.99]])

    pmm = ProbMotionModel(v_mu, v_sigma, theta_dot_mu, theta_dot_sigma, trans_prob)

    hm_gazebo = HumanMotion_Gazebo('cylinder', pmm)
    hm_gazebo.walk(rate)
    # listener()
