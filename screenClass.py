import pygame, widget, cell, random
pygame.init()

class Screen(pygame.sprite.Sprite):
	## A pygame Sprite object which is used to create seperate screens for the game
	def __init__(self, bgColour, buttonsArgs, slidersArgs, textBoxesArgs):
		super().__init__()

		self.bgColour = bgColour
		self.generated = False

		self.image = pygame.Surface([1000, 1000])
		self.image.fill(self.bgColour)
		
		self.rect = self.image.get_rect()

		## Create a new group for each type of widget
		self.buttons = pygame.sprite.Group()
		self.sliders = pygame.sprite.Group()
		self.textBoxes = pygame.sprite.Group()

		## Add the widgets to pygame Groups
		for button in buttonsArgs:
			self.buttons.add(button)

		for slider in slidersArgs:
			self.sliders.add(slider)

		for textBox in textBoxesArgs:
			self.textBoxes.add(textBox)

	def getIndex(self, x, y):
		## Returns the index of a cell in the cells list,
		## given its x and y coorindates

		## Check if the cell is outside the bounds of the maze
		if x < 0 or y < 0 or x > (len(self.cells) ** 0.5) - 1 or y > (len(self.cells) ** 0.5) - 1:
			return -1
		return int(x + y * (len(self.cells) ** 0.5))

	def getXY(self, index):
		## Returns the x and y coordinates of a cell,
		## given its index in the cells list

		width = len(self.cells) ** 0.5
		x = int(index % width)
		y = int(index // width)

		return x, y

class MazeScreen(Screen):
	## A child class of Screen which is used specifically to display
	## the mazes in the main game
	def __init__(self, bgColour, wallColour, difficulty):
		super().__init__(bgColour, [], [], [])

		self.wallColour = wallColour
		self.difficulty = difficulty	
		self.cells = []

	def getNeighbours(self, cell):
		## Returns a list of unvisited cells which neighbour the input cell

		neighbours = []

		## Get the indices of the neighbouring cells
		north = self.getIndex(cell.x, cell.y-1)
		east  = self.getIndex(cell.x-1, cell.y)
		south = self.getIndex(cell.x, cell.y+1)
		west  = self.getIndex(cell.x+1, cell.y)

		## Add each cell to the list of neighbours if it hasn't been visited,
		## and is inside the grid
		if north != -1 and not self.cells[north].visited:
			neighbours.append(self.cells[north])
		if east != -1 and not self.cells[east].visited:
			neighbours.append(self.cells[east])
		if south != -1 and not self.cells[south].visited:
			neighbours.append(self.cells[south])
		if west != -1 and not self.cells[west].visited:
			neighbours.append(self.cells[west])

		return neighbours

	def removeWalls(self, cell1, cell2):
		## Removes the wall between cell1 and cell2

		xDiff = cell2.x - cell1.x
		if xDiff == 1:
			cell1.walls[1] = 0
			cell2.walls[3] = 0
		elif xDiff == -1:
			cell2.walls[1] = 0
			cell1.walls[3] = 0

		yDiff = cell2.y - cell1.y
		if yDiff == 1:
			cell1.walls[2] = 0
			cell2.walls[0] = 0
		elif yDiff == -1:
			cell2.walls[2] = 0
			cell1.walls[0] = 0

	def drawMaze(self, SCREENWIDTH):
		## Draws the maze onto the image attribute of the object,
		## once the maze has been generated

		## Calculate the offset by finding the difference between the width of the screen and the maze
		self.offset = offset = int((SCREENWIDTH - ((len(self.cells) ** 0.5) * self.cellWidth)) / 2)

		## Fill the image black to make a border
		self.image.fill((0, 0, 0))
		## Draw the background in the specified background colour
		pygame.draw.rect(self.image, self.bgColour, (offset, offset, SCREENWIDTH-offset*2, SCREENWIDTH-offset*2))

		for cell in self.cells:
			## Add offset so that each square is shifted slightly to the centre
			i = (cell.x * self.cellWidth) + offset
			j = (cell.y * self.cellWidth) + offset

			## Draw each individual wall of the cell
			if cell.walls[0]:
				pygame.draw.line(self.image, self.wallColour, (i, j), (i+self.cellWidth, j))
			if cell.walls[1]:
				pygame.draw.line(self.image, self.wallColour, (i+self.cellWidth, j), (i+self.cellWidth, j+self.cellWidth))
			if cell.walls[2]:
				pygame.draw.line(self.image, self.wallColour, (i, j+self.cellWidth), (i+self.cellWidth, j+self.cellWidth))
			if cell.walls[3]:
				pygame.draw.line(self.image, self.wallColour, (i, j), (i, j+self.cellWidth))

	def generateMaze(self, SCREENWIDTH, SCREENHEIGHT):
		## Generates a random maze using the Depth First Search algorithm,
		## to fit in the bounds of the screen

		self.generated = True
		self.cellWidth = int(SCREENWIDTH / (8 + int(1.4 * self.difficulty)))

		## Fill self.cells with new cells
		for i in range(int(SCREENWIDTH / self.cellWidth)):
			for j in range(int(SCREENHEIGHT / self.cellWidth)):
				self.cells.append(cell.Cell(j, i))

		## Initialise the stack with the first cell
		current = self.cells[0]
		current.visited = True
		stack = [current]

		## Depth-first search
		while len(stack) > 0:
			## Get all unvisited neighbours
			possibles = self.getNeighbours(current)
			## If it's a dead end, backtrack
			if len(possibles) == 0:
				current = stack.pop()
			else:
				## Randomly choose the next direction
				nextCell = random.choice(possibles)

				## Remove the walls between the cells
				self.removeWalls(current, nextCell)

				## Set the next cell to current and push to the stack
				current = nextCell
				current.visited = True
				stack.append(current)

		## Draw the generated maze onto the image attribute
		self.drawMaze(SCREENWIDTH)

	def reconstructPath(self, cameFrom, current, start):
		## Reconstructs the path which was taken through the maze,
		## in order to get the solution to the maze.
		## Used in the A* algorithm

		path = [current]
		## Loop thorugh the list until the start is reached
		while current != start:
			## Add the current cell to the path list
			current = cameFrom[self.getIndex(current[0], current[1])]
			path.append(current)

		return path[::-1]  ## Return the path in reverse

	def solveGetNeighbours(self, current):
		## Returns a list of cells which can be moved into.
		## Used in the A* algorithm

		possibles = []

		## Get the index of the neighbouring cells
		n = self.getIndex(current.x, current.y-1)
		e = self.getIndex(current.x+1, current.y)
		s = self.getIndex(current.x, current.y+1)
		w = self.getIndex(current.x-1, current.y)

		## Check if each cell is inside the bounds of the maze
		## and there is no wall between
		if n != -1 and not current.walls[0]:
			possibles.append(n)
		if e != -1 and not current.walls[1]:
			possibles.append(e)
		if s != -1 and not current.walls[2]:
			possibles.append(s)
		if w != -1 and not current.walls[3]:
			possibles.append(w)

		return possibles

	def h(self, current, target):
		## Returns the Euclidian distance between current and target
		## 'current' and 'target' are tuples of co-ordinates, (x, y)

		a = abs(current[0] - target[0])
		b = abs(current[1] - target[1])

		c = ((a ** 2) + (b ** 2)) ** 0.5  ## a^2 + b^2 = c^2
		return c

	def aStar(self, start, target):
		## Generates a path from start to target, 
		## given start and target as tuples of co-ordinates (x, y)

		## Get the index of the start sqaure
		currentIndex = self.getIndex(start[0], start[1])

		openSet = [start]
		cameFrom = [0 for i in range(len(self.cells))]

		gScore = [9999 for i in range(len(self.cells))]
		gScore[currentIndex] = 0

		fScore = [9999 for i in range(len(self.cells))]
		fScore[currentIndex] = self.h(start, target)

		while len(openSet) > 0:
			## Set current to the cell in openSet with the lowest fScore
			currentMin = 999
			for value in openSet:
				if fScore[self.getIndex(value[0], value[1])] < currentMin:
					currentMin = fScore[self.getIndex(value[0], value[1])]
					current = value
			currentIndex = self.getIndex(current[0], current[1])

			if current == target:
				## Reconstruct path taken when the target is reached
				return self.reconstructPath(cameFrom, current, start)

			openSet.remove(current)
			for neighbour in self.solveGetNeighbours(self.cells[currentIndex]):
				tentativeG = gScore[currentIndex] + 1
				if tentativeG < gScore[neighbour]:
					## Move to neighbour if it's gScore is lower
					cameFrom[neighbour] = current
					## Recalculate gScore and fScore
					gScore[neighbour] = gScore[currentIndex]
					fScore[neighbour] = gScore[currentIndex] + self.h(current, target)

					## Add to openSet
					if self.getXY(neighbour) not in openSet:
						openSet.append((self.getXY(neighbour)))

	def moveComputer(self, computer):
		## Move the computer to the next square in the optimal path

		if len(self.computerPath) > 0:
			nextSquare = self.computerPath.pop(0)
			computer.gridX = nextSquare[0]
			computer.gridY = nextSquare[1]

			computer.rect.x = computer.gridX * computer.width + self.offset + 1
			computer.rect.y = computer.gridY * computer.width + self.offset + 1

	def moveUser(self, key, player):
		## Moves the character based on which key is pressed

		## Check which key has been pressed, and check there is not a wall in the way
		if key == pygame.K_w and not self.cells[self.getIndex(player.gridX, player.gridY)].walls[0]:
			player.gridY -= 1
		elif key == pygame.K_d and not self.cells[self.getIndex(player.gridX, player.gridY)].walls[1]:
			player.gridX += 1
		elif key == pygame.K_a and not self.cells[self.getIndex(player.gridX, player.gridY)].walls[3]:
			player.gridX -= 1
		elif key == pygame.K_s and not self.cells[self.getIndex(player.gridX, player.gridY)].walls[2]:
			player.gridY += 1

		## Move the coordinates of the player's rectangle
		player.rect.x = player.gridX * player.width + self.offset + 1
		player.rect.y = player.gridY * player.width + self.offset + 1

	def getFinish(self, player, computer):
		## Returns a finish point equidistant from player and computer

		## Get the coordinates of the player and the computer
		playerCoords = (player.gridX, player.gridY)
		computerCoords = (computer.gridX, computer.gridY)

		path = self.aStar(playerCoords, computerCoords)
		return path[len(path) // 2]

	def getWinner(self, player, computer, finish):
		## Check if a player has won the game,
		## return the player who has won, or False if no-one has won

		if player.gridX == finish[0] and player.gridY == finish[1]:
			return "player"
		if computer.gridX == finish[0] and computer.gridY == finish[1]:
			return "computer"
		return False
