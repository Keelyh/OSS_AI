from math import *
from particle import *
from particle_filter import *
from robot import *

N = 100
error = 1.0
bearing_noise = 0.1
for num in range(N):
	error_bearing = num * 10.0 / N * 2
	error *= (exp(-error_bearing/2))
	#print error_bearing, error

#prob = 1.0
#for num in range(N):
#	if num == 0:
#		num = 1
#	error_bearing = num * 10.0 / N * 2
#	prob *= error_bearing**(-2)
#	print error_bearing, prob

#p1 = particle()
#p1.set(45, 25, pi/3)
#p1.particle_measure2()
#p2 = particle()
#p2.set(15, 45, pi/6)
#p2.particle_measure2()

mo = [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0]
me = [[-1, 3.75, -1], [-1, 3.75, -1], [10, 3.75, -1], [9, 3.75, -1], [8, 3.75, -1],
		[7, 3.75, -1], [6, 3.75, -1], [5.1, 3.75, -1], [-1, -1, 3.75], [-1, 3.75, 3.75], 
		[-1, 3.75, 3.75], [-1, 3.75, 3.75], [-1, 3.75, 3.75], [-1, 3.75, 3.75], [-1, 3.75, 3.75]]

#[pos, plot_x, plot_y] = particle_filter(mo,me, 10000, [75, 8, pi/2])

r = robot()
r.measure()
r.one_eighty()


"""
start_pos = [5, 50, 3*pi/2]
[mo, me] = wander_loop(60)
[x, y, theta] = particle_filter(mo, me, 20000, start_pos)
print x, y, theta
"""

"""
x = 25
y = 11
theta = pi / 2
r = robot()
r.set(x, y, theta)
goal = r.goal01
policy = r.dynamic_programming(goal)
print policy
r.execute_path(policy, goal)
print r.x, r.y, r.orientation
"""


"""
r = robot()
r.set(21, 45, 0)
goal = r.goal05
policy = r.dynamic_programming(goal)
print policy
r.execute_path(policy, goal)
print r.x, r.y, r.orientation
"""