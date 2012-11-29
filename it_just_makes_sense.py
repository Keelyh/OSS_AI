from robot import *
import time

vrobot = robot()
for i in range(150):
	vrobot.measure()
	print "Sensing:"
	print vrobot.f_sensor
	print vrobot.r_sensor
	print vrobot.l_sensor
	if vrobot.f_sensor < 3:
		vrobot.stop()
	else:
		vrobot.forward()

vrobot.stop()
