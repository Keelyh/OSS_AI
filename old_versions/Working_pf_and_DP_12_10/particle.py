from math import *
import serial
import time
import random


class particle:
	
	def __init__(self, length = 6.75):
		self.f_sensor = -1
		self.r_sensor = -1
		self.l_sensor = -1
		self.sensor_width = 3.0
		self.x = random.random() * 80 # initial x position
		self.y = random.random() * 80 # initial y position
		self.orientation = random.choice([0, pi/2, pi, 3* pi / 2])# initial orientation
		self.length = length # length of robot
		self.ld = 2.0625 # little distance
		self.bearing_noise  = 0.0 # initialize bearing noise to zero
		self.steering_noise = 0.0 # initialize steering noise to zero
		self.distance_noise = 0.0 # initialize distance noise to zero
		self.oor = -1 # out of range 
		self.oor_dist = 10.1
#		self.worldv = [[1,1,0,1],
#					   [1,0,0,1],
#					   [1,1,0,1]]
#		self.worldh = [[1,1,1],
#					   [1,0,1],
#					   [1,0,1],
#					   [1,1,1]]
		self.worldv = [[1, 0, 0, 0, 0, 0, 1, 0, 1],
						[1, 0, 1, 1, 0, 1, 1, 1, 1],
						[1, 1, 0, 0, 1, 1, 0, 0, 1],
						[1, 1, 0, 0, 0, 0, 1, 1, 1],
						[1, 0, 0, 1, 1, 0, 0, 0, 1],
						[1, 0, 0, 1, 0, 1, 0, 0, 1],
						[1, 1, 0, 1, 0, 1, 0, 0, 1],
						[1, 0, 1, 0, 1, 1, 1, 0, 1]];
		self.worldh = [[1, 1, 1, 1, 1, 1, 1, 1],
						[1, 0, 1, 1, 1, 0, 0, 0],
						[1, 0, 0, 0, 0, 0, 0, 0],
						[0, 0, 1, 1, 0, 0, 0, 0],
						[0, 0, 1, 0, 0, 1, 0, 1],
						[1, 1, 0, 0, 0, 1, 1, 0],
						[0, 1, 0, 0, 1, 0, 1, 1],
						[0, 0, 0, 0, 0, 0, 1, 0],
						[1, 1, 1, 1, 1, 1, 1, 1]]
		
	def set(self, new_x, new_y, new_orientation):

		if new_orientation < 0 or new_orientation >= 2 * pi:
			raise ValueError, 'Orientation must be in [0..2pi]'
		self.x = float(new_x)
		self.y = float(new_y)
		self.orientation = float(new_orientation)
        
	def set_noise(self, new_b_noise, new_s_noise, new_d_noise):
		# makes it possible to change the noise parameters
		# this is often useful in particle filters
		self.bearing_noise  = float(new_b_noise)
		self.steering_noise = float(new_s_noise)
		self.distance_noise = float(new_d_noise)
        
	def measurement_prob(self, measurements):
		# measurements is what the robot is seeing
        # calculate the correct measurement (of the particle)
		predicted_measurements = self.particle_measure() 

		#print "Coordinates:\t" + str(self.x) + "\t" + str(self.y) + "\t" + str(self.orientation)
		#print "Particle Measurements:\t" + str(predicted_measurements[0]) + "\t" + str(predicted_measurements[1]) + "\t" + str(predicted_measurements[2])
		#print "Actual Measurements:\t" + str(measurements[0]) + "\t" + str(measurements[1]) + "\t" + str(measurements[2])
		# compute errors
		prob = 1.0
		for i in range(len(measurements)):
			if (measurements[i] == predicted_measurements[i]):
				error_bearing = 0.1
			elif (measurements[i] == -1 or  predicted_measurements[i] == -1):
				error_bearing = 3
			else:
				error_bearing = abs(measurements[i] - predicted_measurements[i])
			#error_bearing = (error_bearing + pi) % (2.0 * pi) - pi # truncate
			# update Gaussian
			#error *= (exp(- (error_bearing ** 2) / (self.bearing_noise ** 2) / 2.0) /  
			#		sqrt(2.0 * pi * (self.bearing_noise ** 2)))
			prob *= (exp(-error_bearing/3))
		return prob


	def move(self, motion):

		# forward 1 inch
		if motion == 0:
			delta_dist = 1
			delta_ang = 0
		# right turn
		elif motion == 1:
			delta_dist = 0
			delta_ang = 3 * pi / 2
		# left turn
		elif motion == 2:
			delta_dist = 0
			delta_ang = pi / 2
		# 180
		else:
			delta_dist = 0
			delta_ang = pi
			
		d = random.gauss(delta_dist, self.distance_noise)
		#alpha = random.gauss(delta_ang, self.steering_noise)
		alpha = 0.0
		if alpha<.001:
			xp = self.x +d*cos(self.orientation)
			yp = self.y +d*sin(self.orientation)            
			thetap = (self.orientation +delta_ang) %(2*pi)
		else:
			B = d/self.length* tan(alpha)
			R = d/B
			cx = self.x - sin(self.orientation)*R
			cy = self.y + cos(self.orientation)*R

			xp = cx + sin(self.orientation+B)*R
			yp = cy - cos(self.orientation+B)*R
			thetap = (self.orientation+B)%(2*pi)
		
		"""
		xp = self.x + delta_dist * cos(self.orientation)
		yp = self.y + delta_dist * sin(self.orientation)
		thetap = (self.orientation + delta_ang) % (2*pi)
		"""
		
		result = particle()
		result.length = self.length
		result.bearing_noise  = self.bearing_noise
		result.steering_noise = self.steering_noise
		result.distance_noise = self.distance_noise
		result.set(xp,yp,thetap)

		return result
		
	
	def particle_measure(self):
		if (self.y >= 80 or self.x >= 80 or self.y <= 0 or self.x <= 0):
			#self.f_sensor = 100
			#self.r_sensor = 100
			#self.l_sensor = 100
			return [1000, 1000, 1000]
		theta = self.orientation
		# Normalize theta to mod pi/2
		if (theta >= 7*pi/4 or theta < pi/4):
			self.set(self.x,self.y,0)
			theta = 0
		elif (theta >= pi/4 and theta < 3*pi/4):
			self.set(self.x,self.y,pi/2)
			theta = pi/2
		elif (theta >= 3*pi/4 and theta <5*pi/4):
			self.set(self.x,self.y,pi)
			theta = pi
		else:
			self.set(self.x,self.y,3*pi/2)
			theta = 3*pi/2
		
		if (theta == 0 or theta == pi/2):
			rel_x = 10 -(self.x % 10)
			rel_y = 10 -(self.y % 10)
		else:
			rel_x = (self.x % 10)
			rel_y = (self.y % 10)
		
		front_flag = False	
		if (theta == 0 or theta == pi):
			if rel_x < 5:
				front_flag = True
		else:
			if rel_y < 5:
				front_flag = True
				
		g_x = int(self.x / 10)
		g_y = int(self.y / 10)
			
		v_height = len(self.worldv) - 1
		h_height = len(self.worldh) - 1
		
		if (theta == 0 and front_flag == True):
			#wall_1 = self.worldv[v_height - g_y][g_x + 1]
			#wall_2 = self.worldv[v_height - g_y][g_x + 2]
			#left = self.worldh[h_height - g_y - 1][g_x + 1]
			#right = self.worldh[h_height - g_y][g_x + 1]
			# front
			if (self.worldv[v_height - g_y][g_x + 1]): #wall_1
				f = rel_x
			elif (self.worldv[v_height - g_y][g_x + 2] and rel_x < 4):
				f = rel_x + 10
			else:
				f = self.oor
			# left
			if (self.worldv[v_height - g_y][g_x + 1]): #wall_1
				l = rel_x * sqrt(2) - self.ld * sqrt(2)
			elif (self.worldh[h_height - g_y - 1][g_x + 1]): #left
				l = rel_y*sqrt(2) - self.ld * sqrt(2)
			else:
				l = self.oor
			# right
			if (self.worldv[v_height - g_y][g_x + 1]): #wall_1
				r = rel_x * sqrt(2) - self.ld * sqrt(2)
			elif (self.worldh[h_height - g_y][g_x + 1]): #right
				r = (10 - rel_y)*sqrt(2) - self.ld * sqrt(2)
			else:
				r = self.oor
			
		elif (theta == pi and front_flag):
			#rel_x = (self.x % 10)
			#rel_y = (self.y % 10)
			#wall_1 = self.worldv[v_height - g_y][g_x]
			#wall_2 = self.worldv[v_height - g_y][g_x - 1]
			#left = self.worldh[h_height - g_y][g_x - 1]
			#right = self.worldh[h_height - g_y - 1][g_x - 1]
			# front
			if (self.worldv[v_height - g_y][g_x]):
				f = rel_x
			elif (self.worldv[v_height - g_y][g_x - 1] and rel_x < 4):
				f = rel_x + 10
			else:
				f = self.oor
			# left
			if (self.worldv[v_height - g_y][g_x]):
				l = rel_x * sqrt(2) - self.ld * sqrt(2)
			elif (self.worldh[h_height - g_y][g_x - 1]):
				l = rel_y*sqrt(2) - self.ld * sqrt(2)
			else:
				l = self.oor
			# right
			if (self.worldv[v_height - g_y][g_x]):
				r = rel_x * sqrt(2) - self.ld * sqrt(2)
			elif (self.worldh[h_height - g_y - 1][g_x - 1]):
				r = (10 - rel_y)*sqrt(2) - self.ld * sqrt(2)
			else:
				r = self.oor
			
		elif (theta == pi/2 and front_flag):
			#wall_1 = self.worldh[h_height - g_y - 1][g_x]
			#wall_2 = self.worldh[h_height - g_y - 2][g_x]
			#left = self.worldv[v_height - g_y - 1][g_x]
			#right = self.worldv[v_height - g_y - 1][g_x + 1]
			# front
			if (self.worldh[h_height - g_y - 1][g_x]):
				f = rel_y
			elif (self.worldh[h_height - g_y - 2][g_x] and rel_y < 4):
				f = rel_y + 10
			else:
				f = self.oor
			# left
			if (self.worldh[h_height - g_y - 1][g_x]):
				l = rel_y * sqrt(2) - self.ld * sqrt(2)
			elif (self.worldv[v_height - g_y - 1][g_x]):
				l = (10 - rel_x)*sqrt(2) - self.ld * sqrt(2)
			else:
				l = self.oor
			# right
			if (self.worldh[h_height - g_y - 1][g_x]):
				r = rel_y * sqrt(2) - self.ld * sqrt(2)
			elif (self.worldv[v_height - g_y - 1][g_x + 1]):
				r = rel_x*sqrt(2) - self.ld * sqrt(2)
			else:
				r = self.oor
			
		elif (theta == 3*pi/2 and front_flag):
			#wall_1 = self.worldh[h_height - g_y][g_x]
			#wall_2 = self.worldh[h_height - g_y + 1][g_x]
			#left = self.worldv[v_height - g_y + 1][g_x +1]
			#right = self.worldv[v_height - g_y + 1][g_x]
			# front
			if (self.worldh[h_height - g_y][g_x]):
				f = rel_y
			elif (self.worldh[h_height - g_y + 1][g_x] and rel_y < 4):
				f = rel_y + 10
			else:
				f = self.oor
			# left
			if (self.worldh[h_height - g_y][g_x]):
				l = rel_y * sqrt(2) - self.ld * sqrt(2)
			elif (self.worldv[v_height - g_y + 1][g_x +1]):
				l = (10 - rel_x)*sqrt(2) - self.ld * sqrt(2)
			else:
				l = self.oor
			# right
			if (self.worldh[h_height - g_y][g_x]):
				r = rel_y * sqrt(2) - self.ld * sqrt(2)
			elif (self.worldv[v_height - g_y + 1][g_x]):
				r = rel_x*sqrt(2) - self.ld * sqrt(2)
			else:
				r = self.oor
		
		elif (theta == 0 and not front_flag):
			#wall = self.worldv[v_height - g_y][g_x + 1]
			#right_1 = self.worldh[h_height - g_y][g_x]
			#right_2 = self.worldv[v_height - g_y + 1][g_x + 1]
			#left_1 = self.worldh[h_height - g_y - 1][g_x]
			#left_2 = self.worldv[v_height - g_y - 1][g_x + 1]
			
			# front
			if (self.worldv[v_height - g_y][g_x + 1]):
				f = rel_x
			else:
				f = self.oor
			# left 
			if (self.worldh[h_height - g_y - 1][g_x]):
				l = rel_y*sqrt(2) - self.ld * sqrt(2)
			elif(self.worldv[v_height - g_y - 1][g_x + 1]):
				l = (rel_x + self.ld) * sqrt(2) - self.ld * sqrt(2)
			else:
				l = self.oor
			# right
			if (self.worldh[h_height - g_y][g_x]):
				r = (10 - rel_y)*sqrt(2) - self.ld * sqrt(2)
			elif(self.worldv[v_height - g_y + 1][g_x + 1]):
				r = (rel_x + self.ld) * sqrt(2) - self.ld * sqrt(2)
			else:
				r = self.oor
			
		elif (theta == pi/2 and not front_flag):
			#wall = self.worldh[h_height - g_y - 1][g_x]
			#right_1 = self.worldv[v_height - g_y][g_x + 1]
			#right_2 = self.worldh[h_height - g_y - 1][g_x + 1]
			#left_1 = self.worldv[v_height - g_y][g_x]
			#left_2 = self.worldh[h_height - g_y - 1][g_x - 1]
			
			# front
			if (self.worldh[h_height - g_y - 1][g_x]):
				f = rel_y
			else:
				f = self.oor
			# left
			if (self.worldv[v_height - g_y][g_x]):
				l = (10 - rel_x)*sqrt(2) - self.ld * sqrt(2)
			elif (self.worldh[h_height - g_y - 1][g_x - 1]):
				l = (rel_y + self.ld) * sqrt(2) - self.ld * sqrt(2)
			else:
				l = self.oor
			# right
			if (self.worldv[v_height - g_y][g_x + 1]):
				r = rel_x*sqrt(2) - self.ld * sqrt(2)
			elif (self.worldh[h_height - g_y - 1][g_x + 1]):
				r = (rel_y + self.ld) * sqrt(2) - self.ld * sqrt(2)
			else:
				r = self.oor
		
		elif (theta == pi and not front_flag):
			#wall = self.worldv[v_height - g_y][g_x]
			#right_1 = self.worldh[h_height - g_y - 1][g_x]
			#right_2 = self.worldv[v_height - g_y - 1][g_x]
			#left_1 = self.worldh[h_height - g_y][g_x]
			#left_2 = self.worldv[v_height - g_y + 1][g_x]
			
			# front
			if (self.worldv[v_height - g_y][g_x]):
				f = rel_x
			else:
				f = self.oor
			# left 
			if (self.worldh[h_height - g_y][g_x]):
				l = rel_y*sqrt(2) - self.ld * sqrt(2)
			elif(self.worldv[v_height - g_y + 1][g_x]):
				l = (rel_x + self.ld) * sqrt(2) - self.ld * sqrt(2)
			else:
				l = self.oor
			# right
			if (self.worldh[h_height - g_y - 1][g_x]):
				r = (10 - rel_y)*sqrt(2) - self.ld * sqrt(2)
			elif(self.worldv[v_height - g_y - 1][g_x]):
				r = (rel_x + self.ld) * sqrt(2) - self.ld * sqrt(2)
			else:
				r = self.oor
				
		else:
			#wall = self.worldh[h_height - g_y][g_x]
			#right_1 = self.worldv[v_height - g_y][g_x]
			#right_2 = self.worldh[h_height - g_y][g_x - 1]
			#left_1 = self.worldv[v_height - g_y][g_x + 1]
			#left_2 = self.worldh[h_height - g_y][g_x + 1]
			
			# front
			if (self.worldh[h_height - g_y][g_x]):
				f = rel_y
			else:
				f = self.oor
			# left
			if (self.worldv[v_height - g_y][g_x + 1]):
				l = (10 -rel_x)*sqrt(2) - self.ld * sqrt(2)
			elif (self.worldh[h_height - g_y][g_x + 1]):
				l = (rel_y + self.ld) * sqrt(2) - self.ld * sqrt(2)
			else:
				l = self.oor
			# right
			if (self.worldv[v_height - g_y][g_x]):
				r = rel_x*sqrt(2) - self.ld * sqrt(2)
			elif (self.worldh[h_height - g_y][g_x - 1]):
				r = (rel_y + self.ld) * sqrt(2) - self.ld * sqrt(2)
			else:
				r = self.oor
		
		if f > self.oor_dist:
			f = self.oor
		if r > self.oor_dist:
			r = self.oor
		if l > self.oor_dist:
			l = self.oor
		
		#self.f_sensor = f
		#self.r_sensor = r
		#self.l_sensor = l
		return [f, r, l]
	
	def particle_measure2(self):
		# return a high sensor value for a particle that is out of bounds
		if (self.y >= 80 or self.x >= 80 or self.y <= 0 or self.x <= 0):
			return [100, 100, 100]

		# Normalize theta to mod pi/2 to determine which of 4 orientations its in
		# Define rel_front, rel_side_r, and rel_theta
		# Determine if there are walls around the robot
		theta  	= self.orientation
		front 	= -1
		front_r = -1
		front_l = -1
		right_1 = -1
		right_2 = -1
		left_1 	= -1
		left_2 	= -1

		g_x = int(self.x / 10)
		g_y = int(self.y / 10)
			
		v_height = len(self.worldv) - 1
		h_height = len(self.worldh) - 1

		# facing right
		if (theta >= 7*pi/4 or theta < pi/4):
			norm_theta 	= 0
			rel_front 	= 10 - (self.x % 10)
			rel_side_r 	= self.y % 10
			if theta >= 7*pi/4:
				rel_theta = 2*pi - theta
			else:
				rel_theta = -theta
			front 	= self.worldv[v_height - g_y][g_x + 1]
			right_1 = self.worldh[h_height - g_y][g_x]
			left_1 	= self.worldh[h_height - g_y - 1][g_x]
			if (front == 0):
				right_2 = self.worldh[h_height - g_y][g_x + 1]
				left_2 = self.worldh[h_height - g_y - 1][g_x + 1]
			if (right_1 == 0):
				front_r = self.worldv[v_height - g_y + 1][g_x + 1]
			if (left_1 == 0):
				front_l = self.worldv[v_height - g_y - 1][g_x + 1]

		# facing up
		elif (theta >= pi/4 and theta < 3*pi/4):
			norm_theta = pi/2
			rel_front = 10 - (self.y % 10)
			rel_side_r = 10 - (self.x % 10)
			front = self.worldh[h_height - g_y - 1][g_x]
			right_1 = self.worldv[v_height - g_y][g_x + 1]
			left_1 = self.worldv[v_height - g_y][g_x]
			rel_theta = -(theta - pi/2)
			if (front == 0):
				right_2 = self.worldv[v_height - g_y - 1][g_x + 1]
				left_2 = self.worldv[v_height - g_y - 1][g_x]
			if (right_1 == 0):
				front_r = self.worldh[h_height - g_y - 1][g_x + 1]
			if (left_1 == 0):
				front_l = self.worldh[h_height - g_y - 1][g_x - 1]
		# facing left
		elif (theta >= 3*pi/4 and theta <5*pi/4):
			norm_theta = pi
			rel_front = self.x % 10
			rel_side_r = 10 - (self.y % 10)
			rel_theta = -(theta - pi)
			front = self.worldv[v_height - g_y][g_x]
			right_1 = self.worldh[h_height - g_y - 1][g_x]
			left_1 = self.worldh[h_height - g_y][g_x]
			if (front == 0):
				right_2 = self.worldh[h_height - g_y - 1][g_x - 1]
				left_2 = self.worldh[h_height - g_y][g_x - 1]
			if (right_1 == 0):
				front_r = self.worldv[v_height - g_y - 1][g_x]
			if (left_1 == 0):
				front_l = self.worldv[v_height - g_y + 1][g_x]
		# facing down
		else:
			norm_theta = 3*pi/2
			rel_front = self.y % 10
			rel_side_r = self.x % 10
			rel_theta = -(theta - 3*pi/2)
			front = self.worldh[h_height - g_y][g_x]
			right_1 = self.worldv[v_height - g_y][g_x]
			left_1 = self.worldv[v_height - g_y][g_x + 1]
			if (front == 0):
				right_2 = self.worldv[v_height - g_y + 1][g_x]
				left_2 = self.worldv[v_height - g_y + 1][g_x +1]
			if (right_1 == 0):
				front_r = self.worldh[h_height - g_y][g_x - 1]
			if (left_1 == 0):
				front_l = self.worldh[h_height - g_y][g_x + 1]

		# return a high sensor value for particles that is in a place the robot
		# cannot physically be 
		if (rel_front < 1.0 or rel_side_r < 2.0 or (10 - rel_side_r) < 2.0):
			return [100, 100, 100]