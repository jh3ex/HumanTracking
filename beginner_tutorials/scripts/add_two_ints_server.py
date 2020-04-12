#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 12:48:30 2020

@author: jing
"""

from beginner_tutorials.srv import AddTwoInts, AddTwoIntsResponse
import rospy

def handle_add_two_ints(req):
    print("Returing [%s + %s = %s]"%(req.a, req.b, (req.a + req.b)))
    return AddTwoIntsResponse(req.a + req.b)


def add_two_ints_server():
    rospy.init_node('add_two_ints_server')
    s = rospy.Service('add_two_ints', AddTwoInts, handle_add_two_ints)
    print("Ready to add two ints.")
    rospy.spin()
    
if __name__ == '__main__':
    add_two_ints_server()
