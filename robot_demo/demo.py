from wander import *
from particle import *
from particle_filter import *
from robot import *


def main():
	position_check = ""
	while (position_check != "yes"):
		if position_check == 'q':	# Check if the user wants to exit the program
			print "I guess we don't feel like it right now :/"
			return
		#measurements =   [[-1,3.75,3.75],[-1,3.75,3.75],
		#				  [-1,3.75,3.75],[-1,3.75,3.75]] 
		#motions = [0,0,0,0]
		[motions, measurements] = wander_loop(50)
		pos = particle_filter(motions, measurements, 20000, [45,75,pi])
	
		print pos		
		position_check = raw_input("Is this Correct? (answer MUST be 'yes' for correct):")
		#pos = [35,35,pi]
	
	r = robot()
	theta = pos[2]
	if (theta >= 7*pi/4 or theta < pi/4):
		theta = 0
	elif (theta >= pi/4 and theta < 3*pi/4):
		theta = pi/2
	elif (theta >= 3*pi/4 and theta <5*pi/4):
		theta = pi
	else:
		theta = 3*pi/2
	r.set(pos[0], pos[1], theta)
	goal = r.goal01
	policy = r.dynamic_programming(goal)
	r.execute_path(policy, goal)



main()
