import random

def wander(forward, right, left):
	# 0 is go forward 
	# 1 is turn right
	# 2 is turn left
	# 3 is do a 180
	if forward >1:
		forward = 0

	if right >1:
		right = 0

	if left >1:
		left = 0

#	switch(left, forward, right)
	#if (left == 0 and forward == 0 and right == 0):
		#print "1"
	#   	motion = random.randint(0,2)
	if (forward == 0):
		motion = 0
	#elif (left == 0 and forward == 0 and right == 1):
	   	#print "2"
	#   	motion = random.choice([0,2])
	elif (left == 0 and forward == 1 and right == 0):
	   	#print "3"
	   	motion = random.choice([1,2])
	elif (left == 0 and forward == 1 and right == 1):
	   	#print "4"
	   	motion = 2
	#elif (left == 1 and forward == 0 and right == 0):
	   	#print "5"
	#   	motion = random.choice([0,1])
	#elif (left == 1 and forward == 0 and right == 1):
	   	#print "6"
	#   	motion = 0
	elif (left == 1 and forward == 1 and right == 0):
	   	#print "7"
	   	motion = 1
	elif (left == 1 and forward == 1 and right == 1):
		#print "8"
		motion = 3
	return motion


data = [[1, [1, 1], [2, 1], 20],[1, [1, 1], [2, 1], 20],
		[6, [1, 2], [1, 3], 1],[1, [3, 1], [1, 1], 10],
		[1, [1, 1], [1, 1], 8],[1, [2, 1], [2, 1], 12],
		[5, [1, 2], [2, 2], 1],[5, [2, 2], [2, 3], 1],
		[2, [3, 2], [1, 2], 1],[4, [1, 2], [1, 2], 2],
		[1, [2, 1], [4, 1], 2],[3, [1, 4], [1, 2], 2],
		[3, [1, 2], [1, 2], 2],[2, [1, 2], [1, 3], 4],
		[1, [3, 1], [2, 1], 6],[5, [1, 2], [1, 2], 1],
		[1, [2, 1], [1, 1], 15],[4, [1, 2], [2, 2], 1],
		[6, [2, 2], [1, 2], 1],[2, [1, 2], [2, 3], 5]]

for i in range(len(data)):
	print data[i]
	print wander(data[i][0],data[i][1][0],data[i][2][0])


def calculate_front(front_distance):

	if (front_distance <4):
		front_num = 1
	elif (front_distance <14):
		front_num = 2
	else:
		front_num = -1
	return front_num

def calculate_sides(front_distance, side_distance):
	elif (front_distance <5):
		side_num == -2
	elif (front_distance>5 && front_distance<10):
		if (side_distance < 7.1):
			side_num = 1
		elif (side_distance<front_distance*math.sqrt(2)+.2&&side_distance>front_distance*math.sqrt(2)-.2)
			side_num = 2
		else:
			side_num = 3
	elif (front_distance>10 && front_distance<15):
		if (side_distance < 7.2):
			side_num = 2
		elif (side_distance>14 && side_distance<21.21):
			side_num = 3
		else:
			side_num = 4
	elif (front_distance>15 && front_distance<20):
		if (side_distance < 7.1):
			side_num = 1
		elif (side_distance>7.07 && side_distance<14.3):
			side_num = 2
		else:
			side_num = 3
	else :
		side_num = -2