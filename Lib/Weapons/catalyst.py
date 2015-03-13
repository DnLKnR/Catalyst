import pygame

class Catalyst:
	def __init__(self, coordinates):
		self.neg_y_bullets = [[coordinates[0],coordinates[1]]]
		self.pos_x_bullets = []
		self.pos_y_bullets = []
		self.neg_x_bullets = []
		self.window_size = [600,600]
		self.color = [0,255,0]
		self.speed = 3
		self.size = 2
	
	def set_window_size(self,x,y):
		self.window_size = [x,y]
	
	def get_size(self):
		return self.size
		
	def set_size(self, size):
		self.size = size
		
	def get_color(self):
		return self.color
		
	def set_color(self, color):
		self.color = color

	def split_x(self,coordinates):
		self.pos_y_bullets.append([coordinates[0],coordinates[1]])
		self.neg_y_bullets.append([coordinates[0],coordinates[1]])
		
	def split_y(self,coordinates):
		self.pos_x_bullets.append([coordinates[0],coordinates[1]])
		self.neg_x_bullets.append([coordinates[0],coordinates[1]])
	
	def impact(self,coordinates,enemy_size):
		pos_x_i = self.collision(self.pos_x_bullets,coordinates,enemy_size)
		if pos_x_i != -1:
			split_x_coord = self.pos_x_bullets.pop(pos_x_i)
			self.split_x(split_x_coord)
			return True
		pos_y_i = self.collision(self.pos_y_bullets,coordinates,enemy_size)
		if pos_y_i != -1:
			split_y_coord = self.pos_y_bullets.pop(pos_y_i)
			self.split_y(split_y_coord)
			return True
		neg_x_i = self.collision(self.neg_x_bullets,coordinates,enemy_size)
		if neg_x_i != -1:
			split_x_coord = self.neg_x_bullets.pop(neg_x_i)
			self.split_x(split_x_coord)
			return True
		neg_y_i = self.collision(self.neg_y_bullets,coordinates,enemy_size)
		if neg_y_i != -1:
			split_y_coord = self.neg_y_bullets.pop(neg_y_i)
			self.split_y(split_y_coord)
			return True
		return False
	
	def redraw(self,screen):
		count = 0
		for i in range(len(self.neg_y_bullets)-1,-1,-1):
			self.neg_y_bullets[i][1] -= self.speed
			if self.out_of_bounds(self.neg_y_bullets[i]):
				del self.neg_y_bullets[i]
			else:
				pygame.draw.circle(screen, self.get_color(), self.neg_y_bullets[i], self.get_size())
				count += 1
		for i in range(len(self.pos_x_bullets)-1,-1,-1):
			self.pos_x_bullets[i][0] += self.speed
			if self.out_of_bounds(self.pos_x_bullets[i]):
				del self.pos_x_bullets[i]
			else:
				pygame.draw.circle(screen, self.get_color(), self.pos_x_bullets[i], self.get_size())
				count += 1
		for i in range(len(self.pos_y_bullets)-1,-1,-1):
			self.pos_y_bullets[i][1] += self.speed
			if self.out_of_bounds(self.pos_y_bullets[i]):
				del self.pos_y_bullets[i]
			else:
				pygame.draw.circle(screen, self.get_color(), self.pos_y_bullets[i], self.get_size())
				count += 1
		for i in range(len(self.neg_x_bullets)-1,-1,-1):
			self.neg_x_bullets[i][0] -= self.speed
			if self.out_of_bounds(self.neg_x_bullets[i]):
				del self.neg_x_bullets[i]
			else:
				pygame.draw.circle(screen, self.get_color(), self.neg_x_bullets[i], self.get_size())
				count += 1
		if count:
			return True
		else:
			return False

	def out_of_bounds(self,coordinates):
		if coordinates[0] > self.window_size[0] or coordinates[1] > self.window_size[1]:
			return True
		elif coordinates[0] < 0 or coordinates[1] < 0:
			return True
		else:
			return False
	
	def collision(self,bullets,coordinates,enemy_size):
		for i in range(0,len(bullets)):
			if bullets[i][1] < -5:
				return False
			var_x = abs(bullets[i][0] - coordinates[0])
			var_y = abs(bullets[i][1] - coordinates[1])
			if var_x < self.size + enemy_size and var_y < self.size + enemy_size:
				return i
		return -1
