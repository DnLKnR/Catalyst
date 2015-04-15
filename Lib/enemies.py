from Lib.Enemy import *
import random

class Enemies:
	def __init__(self):
		self.color = [255,0,0]
		self.size = 6
		self.rate = 1
		self.enemies = []
		self.window_size = [600,600]
	
	def set_window_size(self,x,y):
		self.window_size = [x,y]
		#Adjust the window size for all the enemies
		for enemy in self.enemies:
			enemy.set_window_size(x,y)
	
	def set_amount(self, amount):
		self.enemies = []
		for i in range(int(amount)):
			#Create a random starting coordinate for the enemy
			x = random.randrange(0, self.window_size[0])
			y = random.randrange(-3000, -50)
			enemy = Enemy([x,y])
			
			#Create random color for enemy as [R,G,B] value
			enemy.set_color([random.randrange(100,255),random.randrange(0,255),random.randrange(0,255)])
			
			#Set the scroll speed for the enemy randomly
			enemy.set_rate(random.randrange(1,4))
			
			#Set a random size for the enemy
			enemy.set_size(random.randrange(4,10) * 2)
			
			#Append the enemy to list of enemies
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
