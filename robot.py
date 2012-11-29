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
		
	def measure(self):
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
			self.measure()
			return
			
		if 200 > sen_data2 or sen_data2 > 225:
			self.measure()
			return

		try:
			sen_data3 = float(sen_data_str3[:6])
		except:
			self.measure()
			return
		
		if 300 > sen_data3 or sen_data3 > 325:
			self.measure()
			return
		
		self.f_sensor = sen_data1 - 100
		self.r_sensor = sen_data2 - 200
		self.l_sensor = sen_data3 - 300
		
		return
		
		
		
