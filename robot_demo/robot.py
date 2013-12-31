from math import *
import serial
import time
import random


class robot:
	
	def __init__(self, length = 6.75):
		self.arduino = serial.Serial('/dev/ttyUSB0', 9600)
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
		self.oor = -1 # out of range value
		self.oor_dist = 10.1
		self.turn_val = 3.25
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
		self.dp_grid = [[0 for row in range(8)] for col in range(8)]
		self.goal01 = [5, 5, pi]		# x and y coordinates, not grid blocks
		self.goal02 = [5, 65, pi]
		self.goal03 = [65, 75, pi/2]
		self.goal04 = [75, 55, 0.0]
		self.goal05 = [65, 5, 3*pi/2]
		
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


	def forward(self):
		# move forward
		self.arduino.write(chr(0))
		print "forward"
		# update robot position
		if self.orientation == 0.0:
			self.x += 1
		elif self.orientation == pi/2:
			self.y += 1
		elif self.orientation == pi:
			self.x -= 1
		else:
			self.y -= 1
	
	def right_turn(self):
		# turn right
		self.arduino.write(chr(1))
		print "right"
		# update robot coordinates
		if self.orientation == 0.0:
			self.x -= self.turn_val
			self.y -= self.turn_val
		elif self.orientation == pi/2:
			self.x += self.turn_val
			self.y -= self.turn_val
		elif self.orientation == pi:
			self.x += self.turn_val
			self.y += self.turn_val
		elif self.orientation == 3 * pi / 2:
			self.x -= self.turn_val
			self.y += self.turn_val
		else:
			print "Error: Did not update right turn coordinates correctly in robot.py"
		self.orientation = (self.orientation + 3 * pi / 2) % ( 2 * pi)

	def left_turn(self):
		# turn left
		self.arduino.write(chr(2))
		print "left"
		# update robot coordinates
		if self.orientation == 0.0:
			self.x -= self.turn_val
			self.y += self.turn_val
		elif self.orientation == pi/2: 
			self.x -= self.turn_val
			self.y -= self.turn_val
		elif self.orientation == pi:
			self.x += self.turn_val
			self.y -= self.turn_val
		elif self.orientation == 3 * pi / 2:
			self.x += self.turn_val
			self.y += self.turn_val
		else:
			print "Error: Did not update right turn coordinates correctly in robot.py"
		self.orientation = (self.orientation + pi / 2) % (2 * pi)

	def one_eighty(self):
		# 180 turn
		self.arduino.write(chr(3))
		print "180"
		# update robot coordinates
		if self.orientation == 0.0:
			self.x -= 2 * self.turn_val
		elif self.orientation == pi/2:
			self.y -= 2 * self.turn_val
		elif self.orientation == pi:
			self.x += 2 * self.turn_val
		else:
			self.y += 2 * self.turn_val
		self.orientation = (self.orientation + pi) % (2 * pi)

	def stop(self):
		self.arduino.write(chr(4))
		
	def pid(self):
		# 5 little right
		# 6 little left
		# right between 3.9 and 4.5
		# left between 3.3 and 3.8
		# if we're too close to the right wall turn a little left
		if (self.r_sensor > 0.0 and self.r_sensor < 3.9) or (self.l_sensor > 3.8 and self.l_sensor < 6.0):
			self.arduino.write(chr(6))
		# if we're too close to the left wall turn a little right
		elif (self.l_sensor > 0.0 and self.l_sensor < 3.3) or (self.r_sensor > 4.5 and self.r_sensor < 6.5):
			self.arduino.write(chr(5))

	def one_measure(self):
		
		for i in range(100):
			sen_data_str1 = str(self.arduino.readline())
			try: 
				sen_data1 = float(sen_data_str1[:6])
				if 100 < sen_data1 and sen_data1 < 125:
					break
			except:
				[f, r, l] = self.one_measure()
				return [f, r, l]
		
		# read the info from the sensors 
		sen_data_str2 = str(self.arduino.readline())
		sen_data_str3 = str(self.arduino.readline())
		
		# cast them to floats
		try: 
			sen_data2 = float(sen_data_str2[:6])
		except:
			[f, r, l] = self.one_measure()
			return [f, r, l]
			
		if 200 > sen_data2 or sen_data2 > 225:
			[f, r, l] = self.one_measure()
			return [f, r, l]

		try:
			sen_data3 = float(sen_data_str3[:6])
		except:
			[f, r, l] = self.one_measure()
			return [f, r, l]
		
		if 300 > sen_data3 or sen_data3 > 325:
			[f, r, l] = self.one_measure()
			return [f, r, l]
			
		if sen_data1 > self.oor_dist + 100:
			sen_data1 = self.oor + 100
		if sen_data2 > self.oor_dist + 200:
			sen_data2 = self.oor + 200
		if sen_data3 > self.oor_dist + 300:
			sen_data3 = self.oor + 300
		
		return [sen_data1 - 100, sen_data2 - 200, sen_data3 - 300]


	def measure(self):

		[f1, r1, l1] = self.one_measure()
		[f2, r2, l2] = self.one_measure()
		[f3, r3, l3] = self.one_measure()
		[f4, r4, l4] = self.one_measure()
		[f5, r5, l5] = self.one_measure()
		[f11, r11, l11] = self.one_measure()
		[f12, r12, l12] = self.one_measure()
		[f13, r13, l13] = self.one_measure()
		[f14, r14, l14] = self.one_measure()
		[f15, r15, l15] = self.one_measure()

		front_total = [f1, f2, f3, f4, f5, f11, f12, f13, f14, f15]
		right_total = [r1, r2, r3, r4, r5, r11, r12, r13, r14, r15]
		left_total =  [l1, l2, l3, l4, l5, l11, l12, l13, l14, l15]	

		front_total.sort()
		right_total.sort()
		left_total.sort() 

		for i in range(2):
			front_total.pop(0)
			right_total.pop(0)
			left_total.pop(0)

		for i in range(2):
			front_total.pop()
			right_total.pop()
			left_total.pop() 

		f_count = 0
		r_count = 0
		l_count = 0
		for j in range(len(front_total)):
			if front_total[j] == -1:
				f_count = 1
			if right_total[j] == -1:
				r_count = 1
			if left_total[j] == -1:
				l_count = 1

		if f_count == 1:
			self.f_sensor = -1
		else:
			self.f_sensor = sum(front_total) / 6.0
		if r_count == 1:
			self.r_sensor = -1
		else:
			self.r_sensor = sum(right_total) / 6.0
		if l_count == 1:
			self.l_sensor = -1
		else:
			self.l_sensor = sum(left_total) / 6.0

	def dynamic_programming(self, goal):
		init = [int(self.x / 10), 7 - int(self.y / 10)]
		goal = [int(goal[0] / 10), 7 - int(goal[1] / 10)]

		delta = [[-1, 0 ], # look up
		         [ 0, -1], # look left
		         [ 1, 0 ], # look down
		         [ 0, 1 ]] # look right

		delta_name = ['^', '<', 'v', '>']

		cost_step = 1 # the cost associated with moving from a cell to an adjacent one.

		value = [[99 for row in range(len(self.dp_grid[0]))] for col in range(len(self.dp_grid))]
		policy = [[' ' for row in range(len(self.dp_grid[0]))] for col in range(len(self.dp_grid))]
		change = True

		v_height = len(self.worldv) - 1
		h_height = len(self.worldh) - 1

		while change:
			change = False

			for y in range(len(self.dp_grid)):
				for x in range(len(self.dp_grid[0])):
					if goal[0] == x and goal[1] == y:
						if value[y][x] > 0:
							value[y][x] = 0
							policy[y][x] = '*'
							change = True

					else:
						for a in range(len(delta)):
							y2 = y + delta[a][0]
							x2 = x + delta[a][1]

							if y2 >= 0 and y2 < len(self.dp_grid) and x2 >= 0 and x2 < len(self.dp_grid[0]):
								wall = -1
								if a == 0:
									wall = self.worldh[h_height - (7 - y) - 1][x]
								elif a == 1:
									wall = self.worldv[v_height - (7 - y)][x]
								elif a == 2:
									wall = self.worldh[h_height - (7 - y)][x]
								else:
									wall = self.worldv[v_height - (7 - y)][x + 1]

								if wall == 0:
									v2 = value[y2][x2] + cost_step

									if v2 < value[y][x]:
										change = True
										value[y][x] = v2
										policy[y][x] = delta_name[a]
		#for j in range(len(value)):
		#	print value[j]
		#for i in range(len(policy)):
		#	print policy[i]
		return policy 

	def execute_path(self, policy, goal):
		self.measure()
		policy_x = int(self.x / 10)
		policy_y = 7 - int(self.y / 10)
		sp = policy[policy_y][policy_x]		# starting policy
		
		# move forward to a spot that is approximately 1.75 away from the next square
		if self.orientation == 0.0:
			rel_f = int(10 - (self.x % 10) - (5 - self.turn_val))
		elif self.orientation == pi/2:
			rel_f = int(10 - (self.y % 10) - (5 - self.turn_val))
		elif self.orientation == pi:
			rel_f = int(self.x % 10 - (5 - self.turn_val))
		else:
			rel_f = int(self.y % 10 - (5 - self.turn_val))
		print rel_f
		for i in range(rel_f):
			self.measure()
			self.pid()
			self.forward()

		# turn so the robot is facing the direction of the staring policy
		if self.orientation == 0.0:
			if sp == '^':
				self.left_turn()
			elif sp == '<':
				self.one_eighty()
			elif sp == 'v':
				self.right_turn()
		elif self.orientation == pi/2:
			if sp == '>':
				self.right_turn()
			elif sp == '<':
				self.left_turn()
			elif sp == 'v':
				self.one_eighty()
		elif self.orientation == pi:
			if sp == '>':
				self.one_eighty()
			elif sp == '^':
				self.right_turn()
			elif sp == 'v':
				self.left_turn()
		elif self.orientation == 3 * pi / 2: 
			if sp == '>':
				self.left_turn()
			elif sp == '^':
				self.one_eighty()
			elif sp == '<':
				self.right_turn()
		else: 
			print "Error: starting orientation inncorrect for DP execution in robot.py"

		# execute the rest of the path
		flag = False
		if rel_f < 0:
			rel_f_flag = True
		else:
			rel_f_flag = False
		while (flag == False):
			policy_x = int(self.x / 10)
			policy_y = 7 - int(self.y / 10)
			if policy[policy_y][policy_x] == '*':
				flag = True
				break
			else:
				# move forward
				n = 10
				if rel_f_flag == True:
					n = 10 + rel_f
					rel_f_flag = False
				for i in range(n):
					self.measure()
					self.pid()
					self.forward()
				new_policy_x = int(self.x / 10)
				new_policy_y = 7 - int(self.y / 10)
				op = policy[policy_y][policy_x]			# old policy
				np = policy[new_policy_y][new_policy_x]	# new policy
				if op != np:
					if (op == '>' and np == 'v') or (op == '^' and np == '>') or (op == '<' and np == '^') or (op == 'v' and np == '<'):
						self.measure()
						self.pid()
						self.right_turn()
					elif (op == '>' and np =='^') or (op == '^' and np == '<') or (op == '<' and np == 'v') or (op == 'v' and np == '>'):
						self.measure()
						self.pid()
						self.left_turn()

		# orient self to goal orientation
		delta_theta = (goal[2] - self.orientation + 2*pi) % (2*pi)
		self.measure()
		self.pid()
		if delta_theta == pi/2:
			self.left_turn()
		elif delta_theta == 3*pi/2:
			self.right_turn()
		elif delta_theta == pi:
			self.one_eighty()

		# run out of the maze
		for i in range(10):
			self.measure()
			self.forward()

		return