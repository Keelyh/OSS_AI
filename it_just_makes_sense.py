from robot import *
import time

vrobot = robot()
for i in range(25):
	vrobot.forward()
	time.sleep(1)
	vrobot.measure()
	print "Sensing:"
	print vrobot.f_sensor
	print vrobot.r_sensor
	print vrobot.l_sensor
