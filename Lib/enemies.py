from Lib.Enemy import *
import random

class Enemies:
	def __init__(self):
		self.color = [255,0,0]
		self.size = 6
		self.rate = 1
		self.enemies = []

	def set_amount(self, amount):
		self.enemies = []
		for i in range(int(amount)):
			x = random.randrange(0, 600)
			y = random.randrange(-3000, -50)
			enemy = Enemy([x,y])
			enemy.set_color([random.randrange(100,255),random.randrange(0,255),random.randrange(0,255)])
			enemy.set_rate(random.randrange(1,4))
			enemy.set_size(random.randrange(4,10) * 2)
			self.enemies.append(enemy)

	def get(self):
		return self.enemies
	
	def get_coords(self):
		return self.enemies
	
	def remove(self, index):
		del self.enemies[index]
	
	def set_color(self, color):
		self.color = color
	
	def get_color(self):
		return self.color

	def is_empty(self):
		if len(self.enemies):
			return False
		return True
	
	def redraw(self, screen):
		for enemy in self.enemies:
			enemy.redraw(screen)