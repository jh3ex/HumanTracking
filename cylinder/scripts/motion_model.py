#!/usr/bin/env python3

import rospy
# from gazebo_msgs.srv import GetModelState, GetModelStateResponse
from gazebo_msgs.srv import SetModelState, GetModelState
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
    def __init__(self, model_name, mu, S, trans_prob):
        self.model_name = model_name
        self.mu = mu
        self.S = S
        self.trans_prob = trans_prob
        
        self.x = ModelState()
        
        self.x.model_name = self.model_name
        self.x.pose.position.x = 0
        self.x.pose.position.y = 0
        self.x.pose.position.z = 0
        self.x.pose.orientation.x = 0
        self.x.pose.orientation.y = 0
        self.x.pose.orientation.z = 0
        self.x.pose.orientation.w = 0
        
    def walk(self):
        # t_1 = self.get_clock()
        
        x, y = self.get_human_state()
        
        self.x.pose.position.x = x + 0.1
        self.x.pose.position.y = y + 0.1
        
        self.set_human_state(self.x)
        
    
    def get_human_state(self):
        rospy.wait_for_service('gazebo/get_model_state')
        
        try:
            get_model_state = rospy.ServiceProxy('gazebo/get_model_state', GetModelState)
            resp1 = get_model_state(self.model_name, 'world')
            
            return resp1.pose.position.x, resp1.pose.position.x
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
        

if __name__ == '__main__':
    hmm = HumanMotionModel('cylinder', 0, 0, 0)
    hmm.walk()
    # listener()
    
