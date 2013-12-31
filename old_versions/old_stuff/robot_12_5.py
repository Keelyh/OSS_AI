from math import *
import serial
import time
import random


class robot:
	
	def __init__(self, length = 7.5):
		self.arduino = serial.Serial('/dev/ttyUSB0', 9600)
		self.f_sensor = -1
		self.r_sensor = -2
		self.l_sensor = -2
		self.x = random.random() * 80 # initial x position
		self.y = random.random() * 80 # initial y position
		self.orientation = random.choice([0, pi/2, pi, 3* pi / 2])# initial orientation
		self.length = length # length of robot
		self.ld = 2.5 # little distance
		self.bearing_noise  = 0.0 # initialize bearing noise to zero
		self.steering_noise = 0.0 # initialize steering noise to zero
		self.distance_noise = 0.0 # initialize distance noise to zero
		self.sd = 3.75 # side distance
		self.oor = 15 # out of range 
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


	def forward(self):
		self.arduino.write(chr(0))
	
	def right_turn(self):
		self.arduino.write(chr(1))
		
	def left_turn(self):
		self.arduino.write(chr(2))
		
	def one_eighty(self):
		self.arduino.write(chr(3))
		
	def stop(self):
		self.arduino.write(chr(4))
		
	def one_measure(self):
		# counts the errors of the sensor input
		error_count = 0
		
		f_sen_data = -2
		r_sen_data = -1
		l_sen_data = -1
		
		for i in range(25):
			sen_data_str1 = str(self.arduino.readline())
			try: 
				sen_data1 = float(sen_data_str1[:6])
				if 100 < sen_data1 and sen_data1 < 125:
					break
			except:
				continue
		
		# read the info from the sensors 
		sen_data_str2 = str(self.arduino.readline())
		sen_data_str3 = str(self.arduino.readline())
		
		# cast them to floats
		try: 
			sen_data2 = float(sen_data_str2[:6])
		except:
			self.one_measure()
			return [0, 0 ,0]
			
		if 200 > sen_data2 or sen_data2 > 225:
			self.one_measure()
			return [0, 0 ,0]

		try:
			sen_data3 = float(sen_data_str3[:6])
		except:
			self.one_measure()
			return [0, 0 ,0]
		
		if 300 > sen_data3 or sen_data3 > 325:
			self.one_measure()
			return [0, 0 ,0]
		
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

		for i in range(3):
			front_total.pop(0)
			right_total.pop(0)
			left_total.pop(0)

		front_total.pop()
		right_total.pop()
		left_total.pop() 

		self.f_sensor = sum(front_total) / 6.0
		self.r_sensor = sum(right_total) / 6.0
		self.l_sensor = sum(left_total) / 6.0
