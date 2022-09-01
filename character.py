import pygame
pygame.init()

class Character(pygame.sprite.Sprite):
	## A pygame Sprite object which is used to create
	## the player and the computer
	def __init__(self, gridX, gridY, width, colour):
		super().__init__()
		
		self.gridX = gridX
		self.gridY = gridY
		self.width = width
		self.colour = colour
		
		## Create the image for the Character
		## and fill it a single colour
		self.image = pygame.Surface([self.width-1, self.width-1])
		self.image.fill(self.colour)
		self.rect = self.image.get_rect()

		## Set the co-ordinates of the character based off its grid position
		self.rect.x = self.gridX * self.width
		self.rect.y = self.gridY * self.width
