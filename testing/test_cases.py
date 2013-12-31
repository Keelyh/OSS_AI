from particle_filter import *

me1 =   [[-1,3.75,3.75],[-1,3.75,3.75],[-1,3.75,3.75],[-1,3.75,3.75],[-1,3.75,3.75],
		 [-1,3.75,3.75],[-1,3.75,3.75],[-1,3.75,3.75],[-1,3.75,3.75],[-1,3.75,3.75],
		 [-1,3.75,3.75],[-1,3.75,3.75],[-1,3.75,3.75],[-1,3.75,3.75],[-1,3.75,3.75],
		 [-1,3.75,3.75],[-1,3.75,3.75],[-1,3.75,3.75],[-1,3.75,3.75],[-1,3.75,3.75],
		 [-1,3.75,-1],[-1,3.75,-1],[-1,3.75,-1],[-1,3.75,-1],[-1,3.75,-1],
		 [-1,3.75,-1],[-1,3.75,-1],[-1,3.75,-1],[-1,3.75,-1],[-1,3.75,-1],
		 [-1,3.75,3.75],[-1,3.75,3.75],[-1,3.75,3.75],[-1,3.75,3.75],[-1,3.75,3.75],
		 [10,3.75,3.75],[9,3.75,3.75],[8,3.75,3.75],[7,3.75,3.75],[6,3.75,3.75],
		 [5,3.75,3.75],[4,3.75,3.75],[3,3.75,3.75],[-1,3.75,3.75],[-1,3.75,3.75]]

mo1 =   [0,0,0,0,0,
		 0,0,0,0,0,
		 0,0,0,0,0,
		 0,0,0,0,0,
		 0,0,0,0,0,
		 0,0,0,0,0,
		 0,0,0,0,0,
		 0,0,3,0,0]

#pos = particle_filter(mo1,me1, 10000, [45, 75, pi])
#print pos
# start at 5,3 facing up!!
measure2 = [[-1,-1,3.75],[-1,-1,3.75],[-1,3.75,3.75],[-1,3.75,3.75],[-1,3.75,3.75], #(5,7)
			[-1,3.75,3.75],[-1,3.57,3.75],[-1,3.75,3.75],[-1,3.75,3.75],[-1,3.75,3.75], #(5,12)
			[-1,3.75,3.75],[-1,3.75,3.75],[-1,-1,3.75],[-1,-1,3.75],[-1,-1,3.75], #(5,17)
			[-1,-1,3.75],[-1,-1,3.75],[10,-1,3.75],[9,-1,3.75],[8,-1,3.75], #(5,22)
			[7,-1,3.75],[6,-1,3.75],[5,-1,3.75],[4,-1,3.75],[3,-1,3.75], #(5,27)
			[2,-1,3.75],[-1,]]

move2 = [0, 0, 0, 0, 0, #(5,8)
		 0, 0, 0, 0, 0, #(5,13)
		 0, 0, 0, 0, 0, #(5,18)
		 0, 0, 0, 0, 0, #(5,23)
		 0, 0, 0, 0, 0, #(5,27)
		 1, 0, 0, 0, 0,]


#pos = particle_filter(move2, measure2, 10000, [5,3,pi/2])
#print pos

#mo = [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0]
me = [[-1, 3.75, -1], [-1, 3.75, -1], [10, 3.75, -1], [9, 3.75, -1], [8, 3.75, -1],
		[7, 3.75, -1], [6, 3.75, -1], [5.1, 3.75, -1], [-1, 3.75, 3.75], [-1, 3.75, 3.75], 
		[-1, 3.75, 3.75], [-1, 3.75, 3.75], [-1, 3.75, 3.75], [-1, 3.75, 3.75], [-1, 3.75, 3.75]]

##mencoder "mf://*.png" -mf fps=3 -o a_video.avi -ovc lavc -lavcopts vcodec=msmpeg4v2:vbitrate=800 

#pos = particle_filter(mo,me, 10000) 
#print pos

[motions, measurements] = wander_loop(50)

pos = particle_filter(motions, measurements, 20000, [75,30,3*pi/2]) 
print pos