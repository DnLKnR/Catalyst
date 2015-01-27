import pygame
import random
import time



class Bullet:
	def __init___(self, coordinates):
		self.coordinates = coordinates
		self.color = [255,0,255]
		self.size = 2
	
	def get(self):
		self.coordinates[1] -= 1
		
	def out_of_bounds(self):
		if self.coordinates[0] > self.window_size[0] and self.coordinates[1] > self.window_size[1]:
			return True
		elif self.coordinates[0] < 0 and self.coordinates[1] < 0:
			return True
		else:
			return False
	
	def impact(self, coordinates):
		var_x = abs(coordinates[0] - self.coordinates[0])
		var_y = abs(coordinates[1] - self.coordinates[1])
		if var_x < self.size and var_y < self.size:
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
	
	def redraw(self):
		if self.out_of_bounds():
			return False
		else:
			pygame.draw.circle(screen, self.get_color(),self.get(),self.get_size())
			return True
	
class Explosive:
	def __init__(self, coordinates):
		self.coordinates = [coordinates[0],coordinates[1]]
		self.explosion_rate = 1
		self.max_explosion_size = 9
		self.speed = 2
		self.size = 2
		self.detonated = 0
		self.color = [0,255,255]
		self.done = 0

	def explode(self):
		self.detonated = 1
		
	def impact(self, coordinates):
		var_x = abs(coordinates[0] - self.coordinates[0])
		var_y = abs(coordinates[1] - self.coordinates[1])
		if var_x < self.size and var_y < self.size:
			self.explode()
			return True
		else:
			return False
	
	def get(self):
		if self.size >= self.max_explosion_size:
			self.done = 1
		elif self.detonated:
			self.size += self.explosion_rate
			self.color = [255,255,0]
		else:
			self.coordinates[1] -= self.speed
	
	def get_color(self)
		return self.color
	
	def get_size(self):
		return self.size
	
	def redraw(self, screen):
		if self.done:
			return False
		elif self.out_of_bounts():
			return False
		else:
			pygame.draw.circle(screen, self.get_color(),self.get(),self.get_size())
			return True
	
	def out_of_bounds(self):
		if self.coordinates[0] > self.window_size[0] and self.coordinates[1] > self.window_size[1]:
			return True
		elif self.coordinates[0] < 0 and self.coordinates[1] < 0:
			return True
		else:
			return False
	
class Catalyst:
	def __init__(self, coordinates):
		self.neg_y_bullets = [coordinates[0],coordinates[1]]
		self.pos_x_bullets = []
		self.pos_y_bullets = []
		self.neg_x_bullets = []
		self.window_size = [600,600]
		self.color = [0,255,0]
		
	def get_color(self):
		return self.color
		
	def set_color(self, color):
		self.color = color

	def split_x(self, coordinates):
		self.pos_y_bullets.append([coordinates[0],coordinates[1]])
		self.neg_y_bullets.append([coordinates[0],coordinates[1]])
		
	def split_y(self, coordinates):
		self.pos_x_bullets.append([coordinates[0],coordinates[1]])
		self.neg_x_bullets.append([coordinates[0],coordinates[1]])
	
	def impact(self, coordinates):
		pos_x_i = self.collision(self.pos_x_bullets,v,enemies.get_size())
		if pos_x_i != -1:
			split_x_coord = self.pos_x_bullets.pop(pos_x_i)
			self.split_x(split_x_coord)
			return
		pos_y_i = self.collision(self.pos_y_bullets,v,enemies.get_size())
		if pos_y_i != -1:
			split_y_coord = self.pos_y_bullets.pop(pos_y_i)
			self.split_y(split_y_coord)
			return
		neg_x_i = self.collision(self.neg_x_bullets,v,enemies.get_size())
		if neg_x_i != -1:
			split_x_coord = self.neg_x_bullets.pop(neg_x_i)
			self.split_x(split_x_coord)
			return
		neg_y_i = self.collision(self.neg_y_bullets,v,enemies.get_size())
		if neg_y_i != -1:
			split_y_coord = self.neg_y_bullets.pop(neg_y_i)
			self.split_y(split_y_coord)
			return
		
	def redraw(self, screen):
		count = 0
		for catalyst in self.neg_y_bullets:
			catalyst[1] -= 1
			if self.out_of_bounds(catalyst):
				continue
			else:
				pygame.draw.circle(screen, self.get_color(), catalyst, self.get_size())
				count += 1
		for catalyst in self.pos_x_bullets:
			catalyst[0] += 1
			if self.out_of_bounds(catalyst):
				continue
			else:
				pygame.draw.circle(screen, self.get_color(), catalyst, self.get_size())
				count += 1
		for catalyst in self.pos_y_bullets:
			catalyst[1] += 1
			if self.out_of_bounds(catalyst):
				continue
			else:
				pygame.draw.circle(screen, self.get_color(), catalyst, self.get_size())
				count += 1
		for catalyst in self.neg_x_bullets:
			catalyst[0] -= 1
			if self.out_of_bounds(catalyst):
				continue
			else:
				pygame.draw.circle(screen, self.get_color(), catalyst, self.get_size())
				count += 1
		if count:
			return True
		return False

	def out_of_bounds(self,coordinates):
		if coordinates[0] > self.window_size[0] and coordinates[1] > self.window_size[1]:
			return True
		elif coordinates[0] < 0 and coordinates[1] < 0:
			return True
		else:
			return False
	
class PowerUps:
	def __init__(self):
		pass

class Bullets:
	def __init__(self):
		self.bullets = []
		self.rate = 0.1
		self.size = 2
		self.distance = 3
		self.color = [0,255,0]
		self.last_bullet_t = time.time()

	def catalyst(self,coordinates):
		if time.time() - self.last_bullet_t > self.rate:
			catalyst_round = Catalyst(coordinates)
			self.bullets.append(catalyst_round)
			self.last_bullet_t = time.time()
			return True
		return False
	
	def explosive(self,coordinates):
		if time.time() - self.last_bullet_t > self.rate:
			explosive_round = Explosive(coordinates)
			self.bullets.append(explosive_round)
			self.last_bullet_t = time.time()
			return True
		return False

	def bullet(self, coordinates):
		if time.time() - self.last_bullet_t > self.rate:
			bullet = Bullet([coordinates[0],coordinates[1]])
			self.bullets.append(bullet)
			self.last_bullet_t = time.time()
	
	def get_rate(self):
		return self.rate
		
	def set_rate(self, value):
		self.rate = value
	
	def get_size(self):
		return len(self.bullets)

	def get_hits(self, enemies):
		all_enemies = enemies.get()
		for i in range(len(all_enemies)-1,-1,-1):
			for bullet in self.bullets:
				if bullet.impact(all_enemies[i]):
					enemies.remove(i)
					break
	
	def out_of_bounds(self, bullets):
		total = []
		for i,v in enumerate(bullets):
			if v[0] > 600 or v[1] > 600:
				total.append(i)
			elif v[0] < 0 or v[1] < 0:
				total.append(i)
		return total

	def set_color(self, color):
		self.color = color
	
	def get_color(self):
		return self.color
	
	def redraw(self, screen):
		for i in range(len(self.bullets)-1,-1,-1):
			if self.bullet[i].redraw(screen):
				continue
			else:
				del bullet[i]
	
	
class Enemies:
	def __init__(self):
		self.color = [255,0,0]
		self.size = 6
		self.rate = 1
		self.enemies = []

	def set_amount(self, amount):
		self.enemies = []
		for i in range(amount):
			x = random.randrange(0, 600)
			y = random.randrange(-600, -10)
			self.enemies.append([x, y])

	def get(self):
		self.reset_out()
		for i in range(len(self.enemies)):
			self.enemies[i][1] += self.rate
		return self.enemies
	
	def get_coords(self):
		return self.enemies
	
	def reset(self, index):
		x = random.randrange(0, 600)
		y = random.randrange(-200, -50)
		self.enemies[index] = [x, y]
		
	def set_size(self, size):
		self.size = size
	
	def get_size(self):
		return self.size

	def reset_out(self):
		for v in self.enemies:
			if v[1] > 600:
				v[1] = random.randrange(-100, -50)
				v[0] = random.randrange(0, 600)
		
	def reset_all(self):
		pass

	def set_rate(self, amount):
		self.rate = amount
	
	def remove(self, index):
		del self.enemies[index]
	
	def set_size(self, size):
		self.size = size
		
	def get_size(self):
		return self.size
	
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
			pygame.draw.circle(screen,self.get_color(),enemy,self.get_size())
		
class Fighter:
	def __init__(self):
		self.Fighter = []
		self.size = 5

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
		
	def set(self, coordinates):
		self.Fighter = [coordinates[0],coordinates[1]]
	
	def get(self):
		return self.Fighter
	
	def hit(self, coordinates):
		#if jet gets hit by bullet or enemies, game over.
		pass
        
class MousePilot:
	def __init__(self):
		self.fighter = Fighter()
		self.enemies = Enemies()
		self.bullets = Bullets()
		self.level = 1
		self.shoot_rate = self.bullets.get_rate()
		self.enemies_created = 200 
		self.enemies.set_amount(self.enemies_created)
		self.window_size = [600, 600]
	
	def level_up(self):
		self.enemies_created += self.enemies_created / 5
		self.enemies.set_amount(self.enemies_created)
		self.shoot_rate += self.shoot_rate * .3
		self.bullets.set_rate(self.shoot_rate)
		self.level += 1
		print('LEVEL-UP: ' + str(self.level))

	def main_loop(self):
		pygame.init()
		screen = pygame.display.set_mode(self.window_size)
		pygame.display.set_caption("Catalyst")
		clock = pygame.time.Clock()
		done = False
		pygame.key.set_repeat(1,1)
		while not done:
			if self.enemies.is_empty():
				self.level_up()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					done = True
				if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or event.type == pygame.MOUSEBUTTONDOWN:
						self.bullets.explosive(self.fighter.get())
			screen.fill([0,0,0])
			self.bullets.get_hits(self.enemies)
			self.bullets.redraw(screen)
			for enemy in self.enemies.get_coords():
				pygame.draw.circle(screen, [255,0,0], enemy, self.enemies.get_size())
			self.fighter.set(pygame.mouse.get_pos())
			pygame.draw.polygon(screen,[255,255,255], self.fighter.get_coords())
			pygame.mouse.set_visible(False)
			pygame.display.flip()
			clock.tick(100)
		pygame.quit()

Game = MousePilot()
Game.main_loop()
