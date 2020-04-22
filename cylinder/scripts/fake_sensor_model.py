#!/usr/bin/env python3
"""
Fake sensor model


Jing Huang
"""


import rospy
# from gazebo_msgs.srv import GetModelState, GetModelStateResponse
from gazebo_msgs.srv import SetModelState, GetModelState
from gazebo_msgs.msg import ModelState
from std_msgs.msg import Float32MultiArray
import numpy as np
from scipy.stats import multivariate_normal
# from cylinder.msg import xy

class FakeSensor:
    def __init__(self, v_mu, v_sigma, target_model):

        self.v_mu = v_mu
        self.v_sigma = v_sigma
        self.target_model = target_model

        # self.state = ModelState()


    def observe(self, pub_rate):

        pub = rospy.Publisher('observation', Float32MultiArray, queue_size=1)
        rospy.init_node('human_control', anonymous=True)
        rate = rospy.Rate(pub_rate)

        msg = Float32MultiArray()
        while not rospy.is_shutdown():
            pos = self.get_fakesensor()
            # Add some noise
            v = multivariate_normal.rvs(mean=self.v_mu, cov=self.v_sigma)
            x = pos.x + v[0]
            y = pos.y + v[1]


            msg.data = [x, y]
            pub.publish(msg)
            rospy.loginfo('Observation [%g, %g]' % (x, y))
            rate.sleep()

    def get_fakesensor(self):
        rospy.wait_for_service('gazebo/get_model_state')

        try:
            get_model_state = rospy.ServiceProxy('gazebo/get_model_state', GetModelState)
            resp1 = get_model_state(self.target_model, 'world')
            # print(resp1)
            return resp1.pose.position
        except rospy.ServiceException:
            print("Service call failed")


if __name__ == '__main__':
    v_mu = np.array([0, 0])
    v_sigma = np.array([[0.05, 0], [0, 0.05]])
    target_model = 'cylinder'
    fs = FakeSensor(v_mu, v_sigma, target_model)

    pub_rate = 0.5
    fs.observe(pub_rate)
