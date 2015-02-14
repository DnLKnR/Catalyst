import pygame

class Bullet:
	def __init__(self, coordinates):
		self.coordinates = [coordinates[0],coordinates[1]]
		self.color = [255,0,255]
		self.size = 2
		self.window_size = [600,600]
		self.done = 0 
		self.speed = 3
		
	def get(self):
		self.coordinates[1] -= self.speed
		return self.coordinates
	
	def out_of_bounds(self):
		if self.coordinates[0] > self.window_size[0] and self.coordinates[1] > self.window_size[1]:
			return True
		elif self.coordinates[0] < 0 and self.coordinates[1] < 0:
			return True
		else:
			return False
	
	def impact(self, coordinates, enemy_size):
		if self.coordinates[1] < -5:
			return False
		var_x = abs(coordinates[0] - self.coordinates[0])
		var_y = abs(coordinates[1] - self.coordinates[1])
		if var_x < self.size + enemy_size and var_y < self.size + enemy_size:
			self.done = 1
			return True
		else:
			return False
	
	def get_color(self):
		return self.color
		
	def set_color(self, color):
		self.color = color
	
	def get_size(self):
		return self.size
		
	def set_size(self, size):
		self.size = size
	
	def get_speed(self, speed):
		return self.speed
	
	def set_speed(self,speed):
		self.speed = speed
	
	def redraw(self, screen):
		if self.out_of_bounds():
			return False
		elif self.done:
			return False
		else:
			pygame.draw.circle(screen,self.get_color(),self.get(),self.get_size())
			return True
