import random
import math
from robot import *

def wander(forward, right, left):
	# 0 is go forward 
	# 1 is turn right
	# 2 is turn left
	# 3 is do a 180
	# 4 is stop
	choices=[]
	if(left ==0):
		choices.append(2)
	if(right ==0):
		choices.append(1)
	if(forward == 0):
		choices.append(0)

	if (len(choices)==0):
		motion = 3
	else:
		motion = random.choice(choices)
	return motion

def calculate_front(front_distance):

	if (front_distance < 5.5 and front_distance != -1):
		front_num = 1
	else:
		front_num = 0
	return front_num

def calculate_sides(front_distance, side_distance):
	if ((side_distance > 5.5 or side_distance == -1) and front_distance >= 4.def foo():
	    doc = "The foo property."
	    def fget(self):
	        return self._foo
	    def fset(self, value):
	        self._foo = value
	    def fdel(self):
	        del self._foo
	    return locals()
	foo = property(**foo()) and front_distance < 6):
		side_num = 0
	else:
		side_num = 1
	return side_num



def wander_loop(iterations):

	motions = []
	measurements = []
	vrobot = robot()
	vrobot.stop()
	old_motion = 4
	for i in range(iterations):
		vrobot.measure()
		print "Sensing:"
		print vrobot.f_sensor
		print vrobot.r_sensor
		print vrobot.l_sensor
		f_num = calculate_front(vrobot.f_sensor)
		r_num = calculate_sides(vrobot.f_sensor, vrobot.r_sensor)
		l_num = calculate_sides(vrobot.f_sensor, vrobot.l_sensor)
		#print "Calculations before motion:"
		#print f_num, r_num, l_num
		motion = wander(f_num, r_num, l_num)


		# 0 is go forward 
		if motion == 0:
			vrobot.forward()
			print "Forward"
			motions.append(0)
			measurements.append([vrobot.f_sensor,vrobot.r_sensor,vrobot.l_sensor])
		# 1 is turn right
		elif motion == 1:
			for i in range(3):
				vrobot.forward()
				print "Forward"
				motions.append(0)
				measurements.append([vrobot.f_sensor,vrobot.r_sensor,vrobot.l_sensor])
			vrobot.right_turn()
			print "Right"
			motions.append(1)
			measurements.append([vrobot.f_sensor,vrobot.r_sensor,vrobot.l_sensor])
		# 2 is turn left
		elif motion == 2:
			for i in range(3):
				vrobot.forward()
				print "Forward"
				motions.append(0)
				measurements.append([vrobot.f_sensor,vrobot.r_sensor,vrobot.l_sensor])
			vrobot.left_turn()
			print "Left"
			motions.append(2)
			measurements.append([vrobot.f_sensor,vrobot.r_sensor,vrobot.l_sensor])
		# 3 is do a 180
		elif motion == 3:
			vrobot.one_eighty()
			print "180"
			motions.append(3)
			measurements.append([vrobot.f_sensor,vrobot.r_sensor,vrobot.l_sensor])
		print
		old_motion = motion


	vrobot.stop()
	return [motions, measurements]
