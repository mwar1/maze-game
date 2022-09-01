class Cell:
	## A basic object which is used to create
	## cells which build up the maze
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.walls = [1, 1, 1, 1]
		self.visited = False
	