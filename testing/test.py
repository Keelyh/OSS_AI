from math import *
a = [.1,.2,.6,1,1.5,2,2.5,3,3.1,3.5,3.8,4]
error = 1
error_bearing =1
for i in a:
	error_bearing = (i + pi) % (2.0 * pi) - pi # truncate
	#print measurements[i], predicted_measurements[i], error_bearing
	# update Gaussian
	#error *= (exp(- (error_bearing ** 2) / (self.bearing_noise ** 2) / 2.0) /  
	#		sqrt(2.0 * pi * (self.bearing_noise ** 2)))
	error *= (exp(- (error_bearing ** 2) / (.01 ** 2) / 2.0) /  
			sqrt(2.0 * pi * (.01 ** 2)))
	print "error", error
