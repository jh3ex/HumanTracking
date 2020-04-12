#!/usr/bin/env python3

import rospy
# from gazebo_msgs.srv import GetModelState, GetModelStateResponse
from gazebo_msgs.srv import *
from gazebo_msgs.msg import ModelState

# def callback(data):
#     rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
#
# def listener():
#     rospy.init_node('listener', anonymous=True)
#     rospy.Subscriber('/human/get_model_state', ModelState, callback)
#
#     rospy.spin()

class HumanMotionModel:
    def __init__(self, mu, S, trans_prob):
        self.mu = mu
        self.S = S
        self.trans_prob = trans_prob
        
        
    def walk(self):
        self.t = get_clock()
        x_t_1 = get_human_state()
        
        
        
        
        
        
        

def get_clock():
    # Get the simulation clock time
    pass
        

def set_human_state(pos):
    rospy.wait_for_service('gazebo/set_model_state')
    
    
    
    try:
        set_model_state = rospy.ServiceProxy('gazebo/set_model_state', GetModelState)
        resp1 = set_model_state('cylinder', 'world')
#        return resp1.pose
    except rospy.ServiceException:
        print("Service call failed")




def get_human_state():
    rospy.wait_for_service('gazebo/get_model_state')
    try:
        get_model_state = rospy.ServiceProxy('gazebo/get_model_state', GetModelState)
        resp1 = get_model_state('cylinder', 'world')
        print(type(resp1.pose.position.x))
        return resp1.pose
    except rospy.ServiceException:
        print("Service call failed")

if __name__ == '__main__':
    get_human_state()
    # listener()
