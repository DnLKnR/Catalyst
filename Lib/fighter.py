class Fighter:
	def __init__(self):
		self.Fighter = [0,0]
		self.size = 5
		self.color = [255,255,255]
		
	def get_coords(self):
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
	
	def hit(self, coordinates, object_size):
		var_x = abs(self.Fighter[0] - coordinates[0])
		var_y = abs(self.Fighter[1] - coordinates[1])
		if var_x < self.size + object_size and var_y < self.size + object_size:
			return True
		else:
			return False

