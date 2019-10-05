import arcade
import sys
import copy
import numpy as np

#function that returns a list of the positions of each cell on the grid
def calculate_positions_of_grid():
    #np grid that stores the positions
    positions = np.empty([num_rows,num_columns,2])
    for i in range(num_rows):
        row = []
        for j in range(num_columns):
            #calculates position of current rectangle
            x = (size_of_margin + width_cell) * j + size_of_margin + width_cell // 2
            y = (size_of_margin + heigth_cell) * i + size_of_margin + heigth_cell // 2
            positions[i][j] = [x,y]
    return positions

def check_boundaries(pos):
	if(pos[0] < 0 or pos[0] > num_columns - 1 or pos[1] < 0 or pos[1] > num_rows - 1 ):
		return True
	return False

def pick_random_move():
	moves = ['up','down','left','right']
	moves = np.random.permutation(moves)
	move = moves[0]
	return move

#receives a label that indicates if the animal is a prey or a predator
def update_grid_position(grid,obj,move):

	aux = copy.deepcopy(obj.body)

	if move == 'up':
		for bp in aux:
			bp[1] -= 1
	elif move == 'down':
		for bp in aux:
			bp[1] += 1
	elif move == 'right':
		for bp in aux:
			bp[0] += 1
	elif move == 'left':
		for bp in aux:
			bp[0] -= 1

	out_of_bounds = False
	for i in aux:
		if check_boundaries(i):
			out_of_bounds = True
			break
	if(not out_of_bounds):
		obj.body = aux

#check if a given position is occupying the space of another
def check_colision(pos,grid):
	pos_x = pos[0]
	pos_y = pos[1]
	if grid[pos_y][pos_x] == 0:
		return False
	else:
		return True

#creates an animal that is not out of bound or colides with another animal
def create_safe_animal(obj,grid):

	#keeps on the loop until it produces an animal that does not goes 
	#out of bounds or colides with another animal
	while True:

		pos_x = np.random.randint(num_columns)
		pos_y = np.random.randint(num_rows)
		obj.position = [pos_x,pos_y]
		obj.constroi_corpo()

		flag_keep_on_loop = False

		for bp in obj.body:

			out_of_bounds = check_boundaries(bp)

			colision = False

			if not out_of_bounds:
				colision = check_colision(bp,grid)

			if out_of_bounds or colision:
				flag_keep_on_loop = True
				break

		if not flag_keep_on_loop:
			break

def populate_grid(grid,num_prey,num_predators):
	#receives imput from user
	num_prey,num_predators = int(sys.argv[1]),int(sys.argv[2])

	#construct the animals
	predators = []
	preys = []

	for i in range(num_predators):

		animal = Predator()
		animal.id = i
		create_safe_animal(animal,grid)

		for bp in animal.body:
			pos_x,pos_y = bp[0],bp[1]
			grid[pos_y][pos_x] = 2

		predators.append(animal)

	for i in range(num_prey):

		animal = Prey()
		animal.id = i
		create_safe_animal(animal,grid)

		for bp in animal.body:
			pos_x,pos_y = bp[0],bp[1]
			grid[pos_y][pos_x] = 1

		preys.append(animal)

	return predators,preys


class Predator():
	def __init__(self):
		self.id = None
		#position of the center of the predator on the grid
		self.position = None
		#colection of cells that composes the animal
		self.body = None

	def constroi_corpo(self):
		positions = np.empty([5])
		down_right = [self.position[0]-1,self.position[1]+1]
		down_left = [self.position[0]-1,self.position[1]-1]
		up_right = [self.position[0]+1,self.position[1]+1]
		up_left = [self.position[0]+1,self.position[1]-1]
		self.body = [self.position,up_left,up_right,down_left,down_right]

class Prey():

	def __init__(self):
		self.id = None
		#position of the center of the predator on the grid
		self.position = None
		#colection of cells that composes the animal
		self.body = None

	def constroi_corpo(self):
		positions = np.empty([5])
		down = [self.position[0],self.position[1]+1]
		up = [self.position[0],self.position[1]-1]
		right = [self.position[0]+1,self.position[1]]
		left = [self.position[0]-1,self.position[1]]
		self.body = [self.position,down,up,left,right]



#inherits from Window class
class DangerZone(arcade.Window):

	def __init__(self,width,heigth,title):
		super().__init__(width,heigth,title)

		#list of cells
		self.shape_list = None

        #list of positions
		self.positions = positions

    	#grid which contains info about each cell, all cells starts empty
		self.grid = []
		for i in range(num_rows):
			row = [0]*num_columns
			self.grid.append(row)

		num_preys,num_predators = sys.argv[1],sys.argv[2]

		#call function that populates the grid with preys and predators
		predators,preys = populate_grid(self.grid,num_preys,num_predators)

		self.predators,self.preys = predators,preys

		arcade.set_background_color(arcade.color.BLACK)

		#draw grid
		self.recreate_grid()

	def recreate_grid(self):

		self.shape_list = arcade.ShapeElementList()

		#transverse grid to check state of each position
		for i in range(num_rows):
			for j in range(num_columns):
				if self.grid[i][j] == 2:
					color = arcade.color.BLUE
				elif self.grid[i][j] == 1:
					color = arcade.color.GREEN
				elif self.grid[i][j] == 0:
					color = arcade.color.WHITE
				
				x = self.positions[i][j][0]
				y = self.positions[i][j][1]
				current_cell = arcade.create_rectangle_filled(x, y, width_cell, heigth_cell, color)
				self.shape_list.append(current_cell)

	def on_draw(self):
		arcade.start_render()
		self.shape_list.draw()

	def update(self,delta_time):

		for predator in self.predators:
			move = pick_random_move()
			update_grid_position(self.grid,predator,move)
	
		for prey in self.preys:
			move = pick_random_move()
			update_grid_position(self.grid,prey,move)
			
		#clean grid
		for i in range(num_rows):
			for j in range(num_columns):
				self.grid[i][j] = 0

		#update positions of predators
		for predators in self.predators:
			for bp in predators.body:
				self.grid[bp[1]][bp[0]] = 2

		#update positions of preys
		for prey in self.preys:
			for bp in prey.body:
				self.grid[bp[1]][bp[0]] = 1

		self.recreate_grid()

num_columns = 70
num_rows = 50
width_cell = 10
heigth_cell = 10
size_of_margin = 2

screen_width = (width_cell + size_of_margin) * num_columns + size_of_margin
screen_heigth = (heigth_cell + size_of_margin) * num_rows + size_of_margin
screen_title = "DangerZone"
positions = calculate_positions_of_grid()

def main():
    DangerZone(screen_width,screen_heigth,screen_title)
    arcade.run()

if __name__ == '__main__':
	main()