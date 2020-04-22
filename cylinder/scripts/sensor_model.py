#!/usr/bin/env python3
"""
Human motion control ros node

Jing Huang
"""


import rospy
from sensor_msgs.msg import Image, PointCloud2
import numpy as np
import cv2
# from cv2 import cv
import sensor_msgs.point_cloud2 as pc2


def callback(image):
    # nparr = np.fromstring(image.data, np.unit8)
    # img_np = cv2.imdecode(nparr, cv2.CV_LOAD_IMAGE_COLOR)
    # #
    # # img_ipl = cv.CreateImageHeader((img_np.shape[1], img_np.shape[0]), cv.IPL_DEPTH_8U, 3)
    # # cv.SetData(img_ipl, img_np.tostring(), img_np.dtype.itemsize * 3 * img_np.shape[1])
    #
    # print(type(image.data))
    # print(type(img_np))
    # print(type(img_ipl))

    # print(image.data)

    gen = pc2.read_points(image, skip_nans=True, field_names=('x', 'y', 'z'))

    n = 0
    for p in gen:
        # print(p[0], p[1])
        n += 1

    print(n)
    print('I have the points!!!!')
    pass

def receiver():
    rospy.init_node('sensor_model', anonymous=True)
    # rospy.Subscriber('/kinect/color/image_raw', Image, callback)
    rospy.Subscriber('/kinect/depth/points', PointCloud2, callback)

    rospy.spin()


if __name__ == '__main__':
    receiver()
