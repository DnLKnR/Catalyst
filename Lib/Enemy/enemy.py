import random, pygame

class Enemy:
	def __init__(self,coordinates):
		self.coordinates = coordinates
		self.color = [255,50,50]
		self.rate = 1
		self.size = 7
		self.window_size = [600,600]
		
	def set_rate(self, rate):
		self.rate = rate
		
	def get_rate(self):
		return self.rate
		
	def set_size(self, size):
		self.size = size
		
	def get_size(self):
		return self.size
		
	def set_color(self, color):
		self.color = color
		
	def get_color(self):
		return self.color
	
	def set_window_size(self, x, y):
		self.window_size = [x,y]
	
	def get(self):
		#Compute the new position and return the coordinates
		self.coordinates[1] += self.rate
		if self.coordinates[1] > self.window_size[1]: 
			return self.reset(self.window_size[0])
		else: 
			return self.coordinates
	
	def get_coord(self):
		return self.coordinates
	
	def reset(self,x_max):
		#Reset the enemy position
		x = random.randrange(0,x_max)
		y = random.randrange(-3000,-50)
		self.coordinates = [x,y]
		return self.coordinates
	
	def redraw(self,screen):
		if self.coordinates[1] < -20:
			return
		pygame.draw.circle(screen,self.get_color(),self.get_coord(),self.get_size())

	
