#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist 
import math

sides_ = {
	'right': 0,
	'front': 0,
	'left': 0,
}

def laser(msg):
	global sides_
	sides_ = {
		'right': min(msg.ranges[0:7]),
		'front': min(msg.ranges[8:12]),
		'left': min(msg.ranges[13:19]),
    }

rospy.init_node('reading_laser')
sub = rospy.Subscriber('/base_scan', LaserScan, laser)
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
while not rospy.is_shutdown():
	msg = Twist() 		
	if sides_['right']>0.7 and sides_['right']<1.2 and sides_['left']>0.7 and sides_['front']>0.7: 
		msg.linear.x = 1
		msg.angular.z = 0	
	if sides_['left']<=0.7:
		msg.linear.x = 0.5
		msg.angular.z = -0.7
	if sides_['right']<=0.7:
		msg.linear.x = 0.5
		msg.angular.z = 0.7 
	if sides_['right']>=1.2:
		msg.linear.x = 0.5
		msg.angular.z = -0.7 
	if sides_['front']<=0.7:
		msg.linear.x = 0.1
		msg.angular.z = 0.7       
	pub.publish(msg)  	
"""pub_ = None
regions_ = {
    'right': 0,
    'fright': 0,
    'front': 0,
    'fleft': 0,
    'left': 0,
}
state_ = 0
state_dict_ = {
    0: 'find the wall',
    1: 'turn left',
    2: 'follow the wall',
}



def clbk_laser(msg):
    global regions_
    regions = {
        'right':  min(min(msg.ranges[0:143]), 4),
        'fright': min(min(msg.ranges[144:287]), 4),
        'front':  min(min(msg.ranges[288:431]), 4),
        'fleft':  min(min(msg.ranges[432:575]), 4),
        'left':   min(min(msg.ranges[576:719]), 4),
    }

    take_action()


def change_state(state):
    global state_, state_dict_
    if state is not state_:
        print 'Wall follower - [%s] - %s' % (state, state_dict_[state])
        state_ = state

def take_action():
	global regions_
	regions = regions_
	msg = Twist()
	linear_x = 0
	angular_z = 0
    
	state_description = ''
    
	d = 1.2

	if regions['front'] > distance and regions['fleft']>0.3 and regions['fright']>0.3:
		state_description = 'case 1 - forward'
		change_state(0)
	elif regions['right'] > distance_l:
		state_description = 'case 2 - right'
		change_state(2)
	elif regions['left'] > distance_l:
		state_description = 'case 3 - left'
		change_state(1)
		rospy.loginfo(regions)

def find_wall():
    msg = Twist()
    msg.linear.x = 0.3
    msg.angular.z = 0.2
    return msg

def turn_left():
    msg = Twist()
    msg.angular.z = 0.6
    return msg

def turn_right():
	msg = Twist()
	msg.angular.z = -0.6

def follow_the_wall():  
    msg = Twist()
    msg.angular.z = 0
    msg.linear.x = 0.3
    return msg

def main():
	global pub_
	rospy.init_node('reading_laser')
	
	pub_ = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
	
	sub = rospy.Subscriber('/base_scan', LaserScan, clbk_laser)

	rate = rospy.Rate(20)
	while not rospy.is_shutdown():
		msg = Twist()
		if state_ == 0:
			msg = find_wall()
		elif state_ == 1:
			msg = turn_left()
		elif state_ == 2:
			msg = follow_the_wall()
			pass
		else:
			rospy.logerr('Unknown state!')

		pub_.publish(msg)

		rate.sleep()





main()"""
