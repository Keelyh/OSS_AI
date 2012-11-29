import random
import math
from robot import *

def wander(forward, right, left):
	# 0 is go forward 
	# 1 is turn right
	# 2 is turn left
	# 3 is do a 180
	# 4 is stop
	if forward >1:
		forward = 0

	if right >1:
		right = 0

	if left >1:
		left = 0

	if (left == 0 and forward == 0 and right == 0):
		#print "1"
	   	motion = random.randint(0,2)
	if (forward == 0 or forward == -1):
		motion = 0
	elif (left == 0 and forward == 0 and right == 1):
	   	#print "2"
	   	motion = random.choice([0,2])
	elif (left == 0 and forward == 1 and right == 0):
	   	#print "3"
	   	motion = random.choice([1,2])
	elif (left == 0 and forward == 1 and right == 1):
	   	#print "4"
	   	motion = 2
	elif (left == 1 and forward == 0 and right == 0):
	   	#print "5"
	   	motion = random.choice([0,1])
	elif (left == 1 and forward == 0 and right == 1):
	   	#print "6"
	   	motion = 0
	elif (left == 1 and forward == 1 and right == 0):
	   	#print "7"
	   	motion = 1
	elif (left == 1 and forward == 1 and right == 1):
		#print "8"
		motion = 3
	else:
		motion = 4
	return motion

def calculate_front(front_distance):

	if (front_distance <4):
		front_num = 1
	elif (front_distance <14):
		front_num = 2
	else:
		front_num = -1
	return front_num

def calculate_sides(front_distance, side_distance):
	a = 4.7
	b = 11.8
	c = 18.8
	d = 1
	if (front_distance < d):
		side_num = -2
	elif (front_distance >= d and front_distance < 10):
		if (side_distance < a):
			side_num = 1
		elif (side_distance < front_distance*math.sqrt(2)+.2 and side_distance>front_distance*math.sqrt(2)-.2):
			side_num = 2
		else:
			side_num = 3
	elif (front_distance>10 and front_distance<15):
		if (side_distance < a):
			side_num = 2
		elif (side_distance > b and side_distance < c):
			side_num = 3
		else:
			side_num = 4
	elif (front_distance > 15 and front_distance < 20):
		if (side_distance < a):
			side_num = 1
		elif (side_distance > a and side_distance < b):
			side_num = 2
		else:
			side_num = 3
	else :
		side_num = -2
		
	return side_num

vrobot = robot()
vrobot.stop()
for i in range(40):
	time.sleep(0.5)
	vrobot.measure()
	print "Sensing:"
	print vrobot.f_sensor
	print vrobot.r_sensor
	print vrobot.l_sensor
	f_num = calculate_front(vrobot.f_sensor)
	r_num = calculate_sides(vrobot.f_sensor, vrobot.r_sensor)
	l_num = calculate_sides(vrobot.f_sensor, vrobot.l_sensor)
	print "Calculations before motion:"
	print f_num, r_num, l_num
	motion = wander(f_num, r_num, l_num)
	print "Motion"
	print motion
	# 0 is go forward 
	if motion == 0:
		vrobot.forward()
		print "Forward"
	# 1 is turn right
	elif motion == 1:
		vrobot.right_turn()
		print "Right"
	# 2 is turn left
	elif motion == 2:
		vrobot.left_turn()
		print "Left"
	# 3 is do a 180
	elif motion == 3:
		vrobot.one_eighty()
		print "180"
	# 4 is stop
	else:
		vrobot.stop()
		print "Stop"
	print
vrobot.stop()




