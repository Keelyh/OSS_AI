import serial
import time

class robot:

	def __init__(self):
		self.arduino = serial.Serial('/dev/ttyUSB0', 9600)
		self.f_sensor = -1;
		self.r_sensor = -2;
		self.l_sensor = -2;
		
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
		counter = 0
		
		f_sen_data = -2
		r_sen_data = -1
		l_sen_data = -1
		
		# read the info from the sensors 
		sen_data_str1 = str(self.arduino.readline())
		sen_data_str2 = str(self.arduino.readline())
		sen_data_str3 = str(self.arduino.readline())
		
		# cast them to floats
		if (sen_data_str1.isspace() == True):
			counter += 1
			sen_data1 = -1
		else:
			sen_data1 = float(sen_data_str1[:6])
		if (sen_data_str2.isspace() == True):
			counter += 1
			sen_data2 = -1
		else:
			sen_data2 = float(sen_data_str2[:6])
		if (sen_data_str3.isspace() == True):
			counter += 1
			sen_data3 = -1
		else:
			sen_data3 = float(sen_data_str3[:6])
		
		# assign them to front, right, and left sensors
		if sen_data1 > 100 and sen_data1 < 200:
			f_sen_data = sen_data1 - 100
		elif sen_data1 > 200 and sen_data1 < 300:
			r_sen_data =  sen_data1 - 200
		elif sen_data1 > 300 and sen_data1 < 400:
			l_sen_data =  sen_data1 - 300
		else:
			counter += 1
		
		if sen_data2 > 100 and sen_data2 < 200:
			f_sen_data = sen_data2 - 100
		elif sen_data2 > 200 and sen_data2 < 300:
			r_sen_data =  sen_data2 - 200
		elif sen_data2 > 300 and sen_data2 < 400:
			l_sen_data =  sen_data2 - 300
		else:
			counter += 1
		
		if sen_data3 > 100 and sen_data3 < 200:
			f_sen_data = sen_data3 - 100
		elif sen_data3 > 200 and sen_data3 < 300:
			r_sen_data =  sen_data3 - 200
		elif sen_data3 > 300 and sen_data3 < 400:
			l_sen_data =  sen_data3 - 300
		else:
			counter += 1
			
		if counter > 0:
			return self.one_measure()
		else:
			return [f_sen_data, r_sen_data, l_sen_data]
	
	def measure(self):
		self.arduino.readline()
		flag = False
		while (flag == False):
			counter = 0
			
			[f1, r1, l1] = self.one_measure()
			[f2, r2, l2] = self.one_measure()
			
			if (f1 - f2) < -0.5 or (f1 - f2) > 0.5 or f1 == -1 or f1 == -2:
				counter += 1
			else:
				f_avg = (f1 + f2) / 2
				
			if (r1 - r2) < -0.5 or (r1 - r2) > 0.5 or r1 == -1:
				counter += 1
			else:
				r_avg = (r1 + r2) / 2
				
			if (l1 - l2) < -0.5 or (l1 - l2) > 0.5 or l1 == -1:
				counter += 1
			else:
				l_avg = (l1 + l2) / 2
			
			if counter == 0:
				self.f_sensor = f_avg
				self.r_sensor = r_avg
				self.l_sensor = l_avg
				flag = True
		return
		
		
