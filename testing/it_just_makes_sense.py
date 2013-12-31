from robot import *
import time

vrobot = robot()
for i in range(50):
	#[f, r, l] = vrobot.one_measure()
	#print l
	vrobot.measure()
	print "Sensing:"
	print vrobot.f_sensor
	print vrobot.r_sensor
	print vrobot.l_sensor


vrobot.stop()


# right between 4 and 4.5 
# left between 3.3 and 3.8