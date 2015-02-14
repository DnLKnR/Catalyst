import random, pygame

class Enemy:
	def __init__(self,coordinates):
		self.coordinates = coordinates
		self.color = [255,50,50]
		self.rate = 1
		self.size = 7
		
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
	
	def get(self):
		self.coordinates[1] += self.rate
		if self.coordinates[1] > 600: 
			return self.reset()
		else: 
			return self.coordinates
	
	def get_coord(self):
		return self.coordinates
	
	def reset(self):
		x = random.randrange(0,600)
		y = random.randrange(-3000,-50)
		self.coordinates = [x,y]
		return self.coordinates
	
	def redraw(self,screen):
		if self.coordinates[1] < -20:
			return
		pygame.draw.circle(screen,self.get_color(),self.get_coord(),self.get_size())

	