#!/usr/bin/env python3

import rospy

import numpy as np
import copy

from std_msgs.msg import Float32MultiArray
from geometry_msgs.msg import Twist
from gazebo_msgs.srv import SetModelState, GetModelState
from gazebo_msgs.msg import ModelState


class BotControl:
    def __init__(self, delta_t, model_name, distance):
        self.delta_t = delta_t
        self.model_name = model_name
        self.distance =distance

        self.pub = rospy.Publisher('/mybot/cmd_vel', Twist, queue_size=1)



    def callback(self, target):

        pos = self.get_bot_state()

        bot_x = pos.x
        bot_y = pos.y

        target_x = target.data[0]
        target_y = target.data[0]

        x_to_go = target_x - bot_x
        y_to_go = target_y - bot_y

        if x_to_go > self.distance:
            vel_x = (x_to_go-self.distance) / self.delta_t * 0.8
        else:
            vel_x = 0.01


        bot_twist = Twist()
        bot_twist.linear.x = vel_x
        self.pub.publish(bot_twist)





    def get_target(self):
        """
        Subscribe to topic '/observation'
        """
        rospy.init_node('bot_control', anonymous=True)

        rospy.Subscriber('/predict_target', Float32MultiArray, self.callback)
        rospy.spin()



    def get_bot_state(self):
        rospy.wait_for_service('gazebo/get_model_state')

        try:
            get_model_state = rospy.ServiceProxy('gazebo/get_model_state', GetModelState)
            resp1 = get_model_state(self.model_name, 'world')
            # print(resp1)
            return resp1.pose.position
        except rospy.ServiceException:
            print("Service call failed")



if __name__ == '__main__':
    delta_t =1
    model_name = 'mybot'
    distance = 0.4
    btc = BotControl(delta_t, model_name, distance)


    btc.get_target()
