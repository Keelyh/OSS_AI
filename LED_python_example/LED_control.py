import serial
import time

arduino = serial.Serial('/dev/ttyUSB0', 9600)

for i in range(10):
	# turn the LED on for 2 seconds
	arduino.write(chr(10))
	time.sleep(2)
	# turn the LED off for 2 seconds
	arduino.write(chr(5))
	time.sleep(2)
