import arcade
import sys
import numpy as np

#function that returns a list of the positions of each cell on the grid
def calculate_positions_of_grid(size_of_margin,width_cell,heigth_cell,num_rows,num_columns):
    #np grid that stores the positions
    positions = np.empty([num_rows,num_columns,2])
    for i in range(num_rows):
        row = []
        for j in range(num_columns):
            #calculates position of current rectangle
            x = (size_of_margin + width_cell) * j + size_of_margin + width_cell // 2
            y = (size_of_margin + heigth_cell) * i + size_of_margin + heigth_cell // 2
            positions[i][j] = (x,y)
    return positions

def check_boundaries(pos,num_rows,num_columns):
	if(pos[0] < 0 or pos[0] > num_columns or pos[1] < 0 or pos[1] > num_rows ):
		return True
	return False
	
class Predator():
	def __init__(self):
		self.id = None
		#position of the center of the predator on the grid
		self.position = None
		#colection of cells that composes the animal
		self.body = None

	def constroi_corpo(self):
		positions = np.empty([5])
		up_left = (self.position[0]-1,self.position[1]+1)
		down_left = (self.position[0]-1,self.position[1]-1)
		up_right = (self.position[0]+1,self.position[1]+1)
		down_right = (self.position[0]+1,self.position[1]-1)
		self.body = [self.position,up_left,up_right,down_left,down_right]

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

		arcade.set_background_color(arcade.color.BLACK)
		#draw grid
		self.recreate_grid()

	def recreate_grid(self):

		self.shape_list = arcade.ShapeElementList()

		#receives imput from user
		num_prey,num_predators = sys.argv[1],sys.argv[2]

		positions_predators = []
		for i in range(int(sys.argv[2])):
			pos_x = np.random.randint(num_columns)
			pos_y = np.random.randint(num_rows)
			positions_predators.append((pos_x,pos_y))

		#construct the predators
		predators = []
		for i in range(len(positions_predators)):

			obj = Predator()
			obj.id = i
			obj.position = positions_predators[i]
			obj.constroi_corpo()

			for bp in obj.body:
				pos_x,pos_y = bp[0],bp[1]
				self.grid[pos_x][pos_y] = 2

			predators.append(obj)

		#transverse grid to check state of each position
		for i in range(num_rows):
			for j in range(num_columns):
				if self.grid[i][j] == 2:
					color = arcade.color.BLUE
				else:
					color = arcade.color.WHITE
				
				x = self.positions[i][j][0]
				y = self.positions[i][j][1]
				current_cell = arcade.create_rectangle_filled(x, y, width_cell, heigth_cell, color)
				self.shape_list.append(current_cell)

	def on_draw(self):
		arcade.start_render()
		self.shape_list.draw()


num_columns = 50
num_rows = 30
width_cell = 15
heigth_cell = 15
size_of_margin = 2

screen_width = (width_cell + size_of_margin) * num_columns + size_of_margin
screen_heigth = (heigth_cell + size_of_margin) * num_rows + size_of_margin
screen_title = "DangerZone"
positions = calculate_positions_of_grid(size_of_margin,width_cell,heigth_cell,num_rows,num_columns)

def main():
    DangerZone(screen_width,screen_heigth,screen_title)
    arcade.run()

if __name__ == '__main__':
	main()