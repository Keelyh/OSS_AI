from robot import *
from wander import *
from particle import *
import matplotlib.pyplot as plt

max_steering_angle = pi / 4.0 # You do not need to use this value, but keep in mind the limitations of a real car.
bearing_noise = 0.1 # Noise parameter: should be included in sense function.
steering_noise = 0.1 # Noise parameter: should be included in move function.
distance_noise = 5.0 # Noise parameter: should be included in move function.

tolerance_xy = 15.0 # Tolerance for localization in the x and y directions.
tolerance_orientation = 0.25 # Tolerance for orientation.

# Gets final position from particle set
def get_position(p):
    x = 0.0
    y = 0.0
    orientation = 0.0
    for i in range(len(p)):
        x += p[i].x
        y += p[i].y
        # orientation is tricky because it is cyclic. By normalizing
        # around the first particle we are somewhat more robust to
        # the 0=2pi problem
        orientation += (((p[i].orientation - p[0].orientation + pi) % (2.0 * pi)) 
                        + p[0].orientation - pi)
    return [x / len(p), y / len(p), orientation / len(p)]



def particle_filter(motions, measurements, N=500): # I know it's tempting, but don't change N!
    # --------
    #
    # Make particles
    # 

	#f = open("data.txt", 'w')
	p = []
	for i in range(N):
		r = particle()
		r.set_noise(bearing_noise, steering_noise, distance_noise)
		p.append(r)
		#f.write("%s\t%s\n" %(r.x, r.y))

    # --------
    #
    # Update particles
    #     

   	real = particle()
   	real.set(55,75,pi)

	for t in range(len(motions)):
		if motions[t] == 1:
			real.set(real.x +cos(real.orientation), real.y +cos(real.orientation), real.orientation) 
		# motion update (prediction)
		# moving every particle for every robot motion
		p2 = []
		#f.write("Next set\n\n")
		plot_x = []
		plot_y = []
		for i in range(N):
			p2.append(p[i].move(motions[t]))
			plot_x.append(p[i].x)
			plot_y.append(p[i].y)
			#f.write("%s\t%s\n" %(r.x, r.y))
		p = p2

		real_x = real.x
		real_y = real.y
		print real_x,real_y

		plt.plot(plot_x, plot_y, '.')
		plt.plot(real_x, real_y, 'ro')

		plt.plot([10,10],[10,20],'k')
		plt.plot([20,20],[0,10],'k')
		plt.plot([10,20],[20,20],'k')
		plt.plot([0,20],[30,30],'k')
		plt.plot([10,10],[40,60],'k')
		plt.plot([30,30],[60,70],'k')
		plt.plot([0,10],[60,60],'k')
		plt.plot([0,10],[70,70],'k')
		plt.plot([20,20],[60,70],'k')	
		plt.plot([30,30],[10,40],'k')
		plt.plot([20,30],[40,40],'k')
		plt.plot([20,40],[50,50],'k')
		plt.plot([20,20],[60,70],'k')
		plt.plot([20,50],[70,70],'k')
		plt.plot([40,40],[0,10],'k')
		plt.plot([40,40],[30,40],'k')
		plt.plot([40,40],[50,60],'k')
		plt.plot([40,50],[20,20],'k')
		plt.plot([50,50],[0,30],'k')
		plt.plot([50,50],[50,70],'k')
		plt.plot([50,60],[30,30],'k')
		plt.plot([50,60],[40,40],'k')
		plt.plot([60,60],[0,10],'k')
		plt.plot([60,60],[40,50],'k')
		plt.plot([60,60],[60,80],'k')
		plt.plot([60,70],[10,10],'k')
		plt.plot([60,80],[20,20],'k')
		plt.plot([60,70],[30,30],'k')
		plt.plot([70,80],[40,40],'k')
		plt.plot([70,70],[40,50],'k')
		plt.plot([70,70],[60,70],'k')

		plt.axis([0, 80, 0, 80],)
		plt.show()
		
		# measurement update
		# getting the probability measurement for each particle
		w = []
		for i in range(N):
			w.append(p[i].measurement_prob(measurements[t]))

		# resampling (reproducing, sex)
		p3 = []
		index = int(random.random() * N)
		beta = 0.0
		mw = max(w)
		for i in range(N):
			beta += random.random() * 2.0 * mw
			while beta > w[index]:
				beta -= w[index]
				index = (index + 1) % N
			p3.append(p[index])
		p = p3

	return [get_position(p), plot_x, plot_y]
 
# IN ORDER TO RUN    
# create a list of motions 
# create a list of measurements 
# run particle filter

# Sarah's simple test case
#mo = [0, 0, 0]
#me = [[15, 3.75, 3.75], [14.5, 3.75, 15], [13.5, 3.75, 15]]
#print particle_filter(mo, me)


#[mo, me] = wander_loop(25)

mo =   [1,1,1,1,1,
		1,1,1,1,1,
		1,1,1,1,1,
		1,1,1,1,1,
		1,1,1,1,1,
		1,1,1,1,1,
		1,1,1,1,1]

me =   [[15,3.75,3.75],[15,3.75,3.75],[15,3.75,3.75],[15,3.75,3.75],[15,3.75,3.75],
		[15,3.75,3.75],[15,3.75,3.75],[15,3.75,3.75],[15,3.75,3.75],[15,3.75,3.75],
		[15,3.75,3.75],[15,3.75,3.75],[15,3.75,3.75],[15,3.75,3.75],[15,3.75,3.75],
		[15,3.75,3.75],[15,3.75,3.75],[15,3.75,3.75],[15,3.75,3.75],[15,3.75,3.75],
		[15,3.75,3.75],[15,3.75,3.75],[15,3.75,3.75],[15,3.75,3.75],[15,3.75,3.75],
		[15,3.75,3.75],[15,3.75,3.75],[15,3.75,3.75],[15,3.75,3.75],[15,3.75,3.75],
		[15,3.75,15],[15,3.75,15],[15,3.75,15],[15,3.75,15],[15,3.75,15]]
[pos, plot_x, plot_y] = particle_filter(mo,me, 50)
print pos

#plt.plot(plot_x, plot_y, 'ro')
#plt.axis([0, 80, 0, 80])
#plt.show()
