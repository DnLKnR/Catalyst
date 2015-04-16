class Fighter:
	def __init__(self):
		self.Fighter = [0,0]
		self.size = 5
		self.color = [255,255,255]
		
	def get_coords(self):
		#Creates the rectangular coordinates for the fighter
		top_left = (self.Fighter[0] - self.size, self.Fighter[1] - self.size)
		top_right = (self.Fighter[0] + self.size, self.Fighter[1] - self.size)
		bottom_left = (self.Fighter[0] - self.size, self.Fighter[1] + self.size)
		bottom_right = (self.Fighter[0] + self.size, self.Fighter[1] + self.size)
		return (top_left,top_right,bottom_right,bottom_left)
		
	def set_size(self, amount):
		self.size = amount
	
	def get_size(self):
		return self.size
		
	def set_color(self, color):
		self.color = color
	
	def get_color(self):
		return self.color
		
	def set(self, coordinates):
		self.Fighter = [coordinates[0],coordinates[1]]
	
	def get(self):
		return self.Fighter
	
	def hit(self, center, radius):
		'''Computes if the fighter is within 
			contact range of the circular enemy'''
		coords = self.get_coords()
		r = radius ** 2
		for coord in coords:
			d =  (coord[0] - center[0]) ** 2 + (coord[1] - center[1]) ** 2
			if d < r: 
				return True
		return False
		