import pygame

class Explosive:
	def __init__(self, coordinates):
		self.coordinates = [coordinates[0],coordinates[1]]
		self.explosion_rate = 2
		self.max_explosion_size = 100
		self.speed = 2
		self.size = 2
		self.detonated = 0
		self.color = [0,255,255]
		self.done = 0
		self.window_size = [600,600]
		self.enemy_speed = 1
				
	def explode(self):
		self.detonated = 1
	
	def set_window_size(self,x,y):
		self.window_size = [x,y]
	
	def impact(self, coordinates, enemy_size):
		if self.coordinates[1] < -5:
			return False
		var_x = abs(coordinates[0] - self.coordinates[0])
		var_y = abs(coordinates[1] - self.coordinates[1])
		if var_x < self.size + enemy_size and var_y < self.size + enemy_size:
			self.explode()
			return True
		else:
			return False
	
	def get(self):
		if self.size >= self.max_explosion_size:
			self.done = 1
		elif self.detonated:
			self.size += self.explosion_rate
			self.coordinates[1] += self.enemy_speed
			self.color = [255,255,0]
		else:
			self.coordinates[1] -= self.speed
		return self.coordinates
	
	def get_color(self):
		return self.color
	
	def get_size(self):
		return self.size
	
	def redraw(self, screen):
		if self.done:
			return False
		elif self.out_of_bounds():
			return False
		else:
			pygame.draw.circle(screen,self.get_color(),self.get(),self.get_size())
			return True
	
	def out_of_bounds(self):
		if self.coordinates[0] > self.window_size[0] and self.coordinates[1] > self.window_size[1]:
			return True
		elif self.coordinates[0] < 0 and self.coordinates[1] < 0:
			return True
		else:
			return False
	
	def set_max_explosion_size(self, size):
		self.max_explosion_size = size
	
