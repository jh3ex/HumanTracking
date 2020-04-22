#!/usr/bin/env python3

import rospy

import numpy as np
import pandas as pd
import copy
from particle_filter import ParticleFilter
from ProbMotionModel import ProbMotionModel
from ProbSensorModel import ProbSensorModel
from std_msgs.msg import Float32MultiArray

class RBE:
    def __init__(self, xt, pf, robot_model):
        self.xt = xt
        self.pf = pf
        self.robot_model = robot_model

        self.pub = rospy.Publisher('predict_target', Float32MultiArray, queue_size=1)
        self.msg = Float32MultiArray()

    def callback(self, pos_msg):
        """
        what we do after get the observation
        """
        
        # Observation
        ox = pos_msg.data[0]
        oy = pos_msg.data[1]

        xtm1 = copy.deepcopy(self.xt)

        self.xt = pf.pf_one_step(self.xt, ox, oy)

        # Orientation correction
        xt_theta, d_walk = pf.re_orientation(xtm1, self.xt)
        if d_walk > 0.6:
            # xt.theta = norm.rvs(xt_theta, 0.001, size=n)
            self.xt.theta = xt_theta



        # Do anohter step of prediction
        xtp1 = self.pf.pmm.prediction(self.xt)

        # Use the prediction to do control
        x_mean = xtp1.x.mean()
        y_mean = xtp1.y.mean()

        # Publish it
        self.msg.data = [x_mean, y_mean]
        self.pub.publish(self.msg)

        rospy.loginfo('Prediction [%g, %g]' % (x_mean, y_mean))




    def get_observation(self):
        """
        Subscribe to topic '/observation'
        """
        rospy.init_node('rbe', anonymous=True)

        rospy.Subscriber('/observation', Float32MultiArray, self.callback)
        rospy.spin()






if __name__ == '__main__':

    np.random.seed(999)

    walk_rd = np.random.RandomState(seed=123)
    """
    Motion model
    """
    n = 1000
    delta_t = 1
    v_mu, v_sigma = 0.5, 0.012
    theta_dot_mu, theta_dot_sigma = 0, 0.02
    trans_prob = np.array([[0.3, 0.7], [0.1, 0.9]])

    pmm = ProbMotionModel(v_mu, v_sigma, theta_dot_mu, theta_dot_sigma, trans_prob, delta_t, n)

    """
    Sensor Model
    """
    ov_mu = np.array([0, 0])
    ov_sigma = np.array([[0.05, 0], [0, 0.05]])

    psm = ProbSensorModel(ov_mu, ov_sigma)
    """
    Initialization of particles
    """
    x0_mu, x0_sigma = 0, 1
    y0_mu, y0_sigma = 0, 1
    theta0_mu, theta0_sigma = 0.0, 0.02

    # Initial particles
    xt = pmm.initial_particles(x0_mu, x0_sigma, y0_mu, y0_sigma, theta0_mu, theta0_sigma)

    """
    Particle Filter
    """
    pf = ParticleFilter(n, pmm, psm)

    robot_model = 'mybot'

    rbe1 = RBE(xt, pf, robot_model)

    rbe1.get_observation()
