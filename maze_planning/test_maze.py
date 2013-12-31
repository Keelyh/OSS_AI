import random

# Vertical walls of the 7x7
world7v = [[0, 0, 0, 0, 0, 0, 0, 0],
		   [0, 0, 0, 0, 0, 0, 0, 0],
		   [0, 0, 0, 0, 0, 0, 0, 0],
		   [0, 0, 0, 0, 0, 0, 0, 0],
		   [0, 0, 0, 0, 0, 0, 0, 0],
		   [0, 0, 0, 0, 0, 0, 0, 0],
		   [0, 0, 0, 0, 0, 0, 0, 0]];

world7h = [[0, 0, 0, 0, 0, 0, 0],
		   [0, 0, 0, 0, 0, 0, 0],
		   [0, 0, 0, 0, 0, 0, 0],
		   [0, 0, 0, 0, 0, 0, 0],
		   [0, 0, 0, 0, 0, 0, 0],
		   [0, 0, 0, 0, 0, 0, 0],
		   [0, 0, 0, 0, 0, 0, 0],
		   [0, 0, 0, 0, 0, 0, 0]]

test_worldv = [[1, 0, 0, 1],
			   [1, 1, 0, 1],
			   [1, 0, 0, 1]]
test_worldh = [[1, 1, 1],
			   [0, 0, 0],
			   [0, 0, 1],
			   [1, 1, 1]]

def print_matrix(matrix):
	for i in range(len(matrix)):
		print matrix[i]
		
def add_matrix(matrix_v, matrix_h):
	counter = 0
	for i in range(2):
		if i == 0:
			matrix = matrix_v
		else:
			matrix = matrix_h
		for i in range(len(matrix)):
			for j in range(len(matrix[0])):
				if matrix[i][j] == 1:
					counter += 1
	return counter
			
def make_maze(world_v, world_h):
	for i in range(len(world_v)):
		for j in range(len(world_v[0])):
			if j == 0 or j == len(world_v[0]) - 1:
				world_v[i][j] = 1
	for i in range(len(world_h)):
		for j in range(len(world_h[0])):
			if i == 0 or i == len(world_h) - 1:
				world_h[i][j] = 1
	# Randomly set the interior wall barriors
	wall_count = add_matrix(world_v, world_h)
	while (wall_count < 69):
		rand_matrix = random.randint(0,1)
		if rand_matrix == 0:
			ir = random.randint(0, len(world_v)-2)
			jr = random.randint(0, len(world_v[0])-2)
			if world_v[ir][jr] != 1 and not (world_v[ir][jr + 1] == 1 and world_h[ir][jr] == 1 and world_h[ir + 1][jr] == 1):
				if ir != 0 and jr != 0:
					if not (world_v[ir][jr - 1] == 1 and world_h[ir + 1][jr - 1] == 1 and world_h[ir][jr - 1] == 1):
						world_v[ir][jr] = 1
						wall_count += 1
				else:
					world_v[ir][jr] = 1
					wall_count += 1
		else:
			ir = random.randint(0, len(world_h)-2)
			jr = random.randint(0, len(world_h[0])-2)
			if world_h[ir][jr] != 1 and not (world_h[ir + 1][jr] == 1 and world_v[ir][jr] == 1 and world_v[ir][jr + 1] == 1):
				if ir != 0 and jr != 0:
					if not (world_h[ir - 1][jr] == 1 and world_v[ir - 1][jr] == 1 and world_v[ir - 1][jr + 1] == 1):
						world_h[ir][jr] = 1
						wall_count += 1
				else:
					world_h[ir][jr] = 1
					wall_count += 1
	return [world_v, world_h]
	
def evaluate_maze(world_v, world_h):
	cell_height = len(world_h)-1
	cell_width = len(world_v[0])-1
	eval_list = []
	temp = 0
	temp_r1 = 0
	temp_r2 = 0
	temp_l1 = 0
	temp_l2 = 0
	for i in range(cell_height):
		for j in range(cell_width):
			for k in range(4):
				# up
				if k == 0:
					# front sensor
					front_count = 1
					for a in range(cell_height):
						# boundary case
						if i - a == 0:
							temp = front_count
							break
						# barrior case
						else:
							if world_h[i - a][j] == 1:
								temp = front_count
								break
							else:
								front_count += 1
					# left sensor 
					left_count1 = 1
					for c in range(5):
						if world_v[i - c][j - c] == 1:
							temp_l1 = left_count1
							break
						else:
							left_count1 += 1
							if world_h[i - c][j - c - 1] == 1:
								temp_l1 = left_count1
								break
							else:
								left_count1 += 1
					left_count2 = 1
					for d in range(5):
						if world_h[i - d][j - d] == 1:
							temp_l2 = left_count2
							break
						else:
							left_count2 += 1
							if world_v[i - d - 1][j - d] == 1:
								temp_l2 = left_count2
								break
							else:
								left_count2 += 1
					right_count1 = 1
					for c in range(5):
						if world_v[i - c][j + c + 1] == 1:
							temp_r1 = right_count1
							break
						else:
							right_count1 += 1
							if world_h[i - c][j + c + 1] == 1:
								temp_r1 = right_count1
								break
							else:
								right_count1 += 1
					right_count2 = 1
					for d in range(5):
						if world_h[i - d][j + d] == 1:
							temp_r2 = right_count2	
							break
						else:
							right_count2 += 1
							if world_v[i - d - 1][j + d + 1] == 1:
								temp_r2 = right_count2
								break
							else:
								right_count2 += 1		
				# right
				elif k == 1:
					# front sensor
					front_count = 1
					for b in range(cell_width):
						# boundary case
						if j + b + 1 <= cell_width:
							if j + b + 1 == cell_width:
								temp = front_count
								break
							# barrior case
							else:
								if world_v[i][j + b + 1] == 1:
									temp = front_count
									break
								else:
									front_count += 1
					# left sensor
					left_count1 = 1
					for c in range(5):
						if world_h[i - c][j + c] == 1:
							temp_l1 = left_count1
							break
						else:
							left_count1 += 1
							if world_v[i - c - 1][j + c + 1] == 1:
								temp_l1 = left_count1
								break
							else:
								left_count1 += 1
					left_count2 = 1
					for d in range(5):
						if world_v[i - d][j + d + 1] == 1:
							temp_l2 = left_count2
							break
						else:
							left_count2 += 1
							if world_h[i - d][j + d + 1] == 1:
								temp_l2 = left_count2
								break
							else:
								left_count2 += 1
					# right sensor
					right_count1 = 1
					for c in range(5):
						if world_h[i + c + 1][j + c] == 1:
							temp_r1 = right_count1
							break
						else:
							right_count1 += 1
							if world_v[i + c + 1][j + c + 1] == 1:
								temp_r1 = right_count1
								break
							else:
								right_count1 += 1
					right_count2 = 1
					for d in range(5):
						if world_v[i + d][j + d + 1] == 1:
							temp_r2 = right_count2	
							break
						else:
							right_count2 += 1
							if world_h[i + d + 1][j + d + 1] == 1:
								temp_r2 = right_count2
								break
							else:
								right_count2 += 1
				# down
				elif k == 2:
					# front sensor
					front_count = 1
					for a in range(cell_height):
						# boundary case
						if i + a + 1 <= cell_height:
							if i + a + 1 == cell_height:
								temp = front_count
								break
							# barrior case
							else:
								if world_h[i + a + 1][j] == 1:
									temp = front_count
									break
								else:
									front_count += 1
					# left sensor
					left_count1 = 1
					for c in range(5):
						if world_v[i + c][j + c + 1] == 1:
							temp_l1 = left_count1
							break
						else:
							left_count1 += 1
							if world_h[i + c + 1][j + c + 1] == 1:
								temp_l1 = left_count1
								break
							else:
								left_count1 += 1
					left_count2 = 1
					for d in range(5):
						if world_h[i + d + 1][j + d] == 1:
							temp_l2 = left_count2
							break
						else:
							left_count2 += 1
							if world_v[i + d + 1][j + d + 1] == 1:
								temp_l2 = left_count2
								break
							else:
								left_count2 += 1
					# right sensor
					right_count1 = 1
					for c in range(5):
						if world_v[i + c][j - c] == 1:
							temp_r1 = right_count1
							break
						else:
							right_count1 += 1
							if world_h[i + c + 1][j - c - 1] == 1:
								temp_r1 = right_count1
								break
							else:
								right_count1 += 1
					right_count2 = 1
					for d in range(5):
						if world_h[i + d + 1][j - d] == 1:
							temp_r2 = right_count2	
							break
						else:
							right_count2 += 1
							if world_v[i + d + 1][j - d] == 1:
								temp_r2 = right_count2
								break
							else:
								right_count2 += 1	
				# left
				else:
					#"""
					# front sensor
					front_count = 1
					for b in range(cell_width):
						# boundary case
						if j - b == 0:
							temp = front_count
							break
						# barrior case
						else:
							if world_v[i][j - b] == 1:
								temp = front_count
								break
							else:
								front_count += 1
					# left sensor
					left_count1 = 1
					for c in range(5):
						if world_h[i + c + 1][j - c] == 1:
							temp_l1 = left_count1
							break
						else:
							left_count1 += 1
							if world_v[i + c + 1][j - c] == 1:
								temp_l1 = left_count1
								break
							else:
								left_count1 += 1
					left_count2 = 1
					for d in range(5):
						if world_v[i + d][j - d] == 1:
							temp_l2 = left_count2
							break
						else:
							left_count2 += 1
							if world_h[i + d + 1][j - d -1] == 1:
								temp_l2 = left_count2
								break
							else:
								left_count2 += 1
					# right sensor
					right_count1 = 1
					for c in range(5):
						if world_h[i - c][j - c] == 1:
							temp_r1 = right_count1
							break
						else:
							right_count1 += 1
							if world_v[i - c - 1][j - c] == 1:
								temp_r1 = right_count1
								break
							else:
								right_count1 += 1
					right_count2 = 1
					for d in range(5):
						if world_v[i - d][j - d] == 1:
							temp_r2 = right_count2	
							break
						else:
							right_count2 += 1
							if world_h[i - d][j - d - 1] == 1:
								temp_r2 = right_count2
								break
							else:
								right_count2 += 1
				found = 0
				if eval_list == []:
					eval_list.append([temp, [temp_l1, temp_l2], [temp_r1, temp_r2], 1])
				else:
					for x in range(len(eval_list)):
						if eval_list[x][0] == temp and eval_list[x][1] == [temp_l1, temp_l2] and eval_list[x][2] == [temp_r1, temp_r2]:
							eval_list[x][3] += 1
							found = 1
				if found == 0:
					eval_list.append([temp, [temp_l1, temp_l2], [temp_r1, temp_r2], 1])
	return eval_list
	
def determine_freq(eval_list):
	counter = 0
	for i in range(len(eval_list)):
		if eval_list[i][3] != 1:
			counter += eval_list[i][3]
	return counter;

maze = [0, 1]
min_freq = 1000
maze_length = 8
maze_width = 8


for y in range(1000):
	world7v = [[0 for row in range(maze_length + 1)] for col in range(maze_width)]
	world7h = [[0 for row in range(maze_length)] for col in range(maze_width + 1)]
	[world_v, world_h] = make_maze(world7v, world7h)
	list_out = evaluate_maze(world_v, world_h)
	output = determine_freq(list_out)
	if output < min_freq:
		maze = [world_v, world_h]
		min_freq = output
		#print output
print_matrix(maze[0])
print
print_matrix(maze[1])
print min_freq

world8v = [[1, 0, 0, 0, 0, 0, 1, 0, 1],
		   [1, 0, 1, 1, 0, 1, 1, 1, 1],
		   [1, 1, 0, 0, 1, 1, 0, 0, 1],
		   [1, 1, 0, 0, 0, 0, 1, 1, 1],
		   [1, 0, 0, 1, 1, 0, 0, 0, 1],
		   [1, 0, 0, 1, 0, 1, 0, 0, 1],
		   [1, 1, 0, 1, 0, 1, 0, 0, 1],
		   [1, 0, 1, 0, 1, 1, 1, 0, 1]];

world8h = [[1, 1, 1, 1, 1, 1, 1, 1],
		   [1, 0, 1, 1, 1, 0, 0, 0],
		   [1, 0, 0, 0, 0, 0, 0, 0],
		   [0, 0, 1, 1, 0, 0, 0, 0],
		   [0, 0, 1, 0, 0, 1, 0, 1],
		   [1, 1, 0, 0, 0, 1, 1, 0],
		   [0, 1, 0, 0, 1, 0, 1, 1],
		   [0, 0, 0, 0, 0, 0, 1, 0],
		   [1, 1, 1, 1, 1, 1, 1, 1]]

my_counter = 0
for t in range(len(world8v)):
	for s in range(len(world8v[0])):
		if world8v[t][s] == 1:
			my_counter += 1
for u in range(len(world8h)):
	for v in range(len(world8h[0])):
		if world8h[u][v] == 1:
			my_counter += 1
print 'My counter'
print my_counter

"""		   
list_out2 = evaluate_maze(world8v, world8h)
print_matrix(list_out2)
output2 = determine_freq(list_out2)
print output2
"""
