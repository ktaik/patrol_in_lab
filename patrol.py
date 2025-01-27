#!/usr/bin/env python2

import rospy, math
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
from std_srvs.srv import Empty

count = 0
goal = PoseStamped()
goal.header.frame_id = 'map'
goal.header.stamp = rospy.Time()
goal.pose.position.x = 2.09351730347
goal.pose.position.y = 6.8
goal.pose.position.z = 0.0
goal.pose.orientation.x = 0.0
goal.pose.orientation.y = 0.0
goal.pose.orientation.z = -0.735359871125
goal.pose.orientation.w = 0.677676810832

def callback(msg):

    global count, goal

    #left
    goal1 = PoseStamped()
    goal1.header.frame_id = 'map'
    goal1.header.stamp = rospy.Time()
    goal1.pose.position.x = 2.09351730347
    goal1.pose.position.y = 6.8
    goal1.pose.position.z = 0.0
    goal1.pose.orientation.x = 0.0
    goal1.pose.orientation.y = 0.0
    goal1.pose.orientation.z = -0.735359871125
    goal1.pose.orientation.w = 0.677676810832

    #right 1.80495929718 1.74022388458
    goal2 = PoseStamped()
    goal2.header.frame_id = 'map'
    goal2.header.stamp = rospy.Time()
    goal2.pose.position.x = 1.77
    goal2.pose.position.y = 1.8
    goal2.pose.position.z = 0.0
    goal2.pose.orientation.x = 0.0
    goal2.pose.orientation.y = 0.0
    goal2.pose.orientation.z = 0.674945648426
    goal2.pose.orientation.w = 0.737867448578
    
    if (count == 0):
        distance_from_goal1 = math.sqrt((msg.pose.pose.position.x - goal1.pose.position.x)**2 + (msg.pose.pose.position.y - goal1.pose.position.y)**2)
        angle1 = (msg.pose.pose.orientation.z - goal1.pose.orientation.z)**2 + (msg.pose.pose.orientation.w - goal1.pose.orientation.w) **2
        if (distance_from_goal1 < 1.0 and angle1 < 0.1): 
            count = 1
        goal = goal1
    if (count == 1):
        distance_from_goal2 = math.sqrt((msg.pose.pose.position.x - goal2.pose.position.x)**2 + (msg.pose.pose.position.y - goal2.pose.position.y)**2)
        angle2 = (msg.pose.pose.orientation.z - goal2.pose.orientation.z)**2 + (msg.pose.pose.orientation.w - goal2.pose.orientation.w) **2
        if (distance_from_goal2 < 1.0 and angle2 < 0.1):
            count = 0
        goal = goal2
        
def main():

    rospy.init_node('main')

    try:
        service = rospy.ServiceProxy('release_brake', Empty)
        service()
    except rospy.ServiceException as e:
        rospy.logerr(e)

    rospy.Subscriber('pose', PoseWithCovarianceStamped, callback)
    pub = rospy.Publisher('move_base_simple/goal', PoseStamped, queue_size=10)

    r = rospy.Rate(1.0)
    while not rospy.is_shutdown():
        pub.publish(goal)
        r.sleep()

if __name__ == '__main__':
    main()