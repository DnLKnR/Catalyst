import pygame
import wx
import random
import time

class PowerUps:
	def __init__(self):
		pass

class Bullets:
	def __init__(self):
		self.pos_x_bullets = []
		self.pos_y_bullets = []
		self.neg_x_bullets = []
		self.neg_y_bullets = []
		self.rate = 0.1
		self.size = 2
		self.distance = 3
		self.color = [0,255,0]
		self.last_bullet_t = time.time()

	def shoot(self, coordinates):
		if time.time() - self.last_bullet_t > self.rate: 
			self.neg_y_bullets.append([coordinates[0],coordinates[1]])
			self.last_bullet_t = time.time()
	
	def clean(self):
		for i in reversed(self.out_of_bounds(self.pos_x_bullets)):
			del self.pos_x_bullets[i]	
		for i in reversed(self.out_of_bounds(self.pos_y_bullets)):
			del self.pos_y_bullets[i]
		for i in reversed(self.out_of_bounds(self.neg_x_bullets)):
			del self.neg_x_bullets[i]
		for i in reversed(self.out_of_bounds(self.neg_y_bullets)):
			del self.neg_y_bullets[i]
	
	def impact(self, enemies):
		self.clean()
		for i,v in enumerate(enemies.get()):
			pos_x_i = self.collision(self.pos_x_bullets,v,enemies.get_size())
			if pos_x_i != -1:
				split_x_coord = self.pos_x_bullets.pop(pos_x_i)
				self.split_x(split_x_coord)
				enemies.remove(i)
				continue
			pos_y_i = self.collision(self.pos_y_bullets,v,enemies.get_size())
			if pos_y_i != -1:
				split_y_coord = self.pos_y_bullets.pop(pos_y_i)
				self.split_y(split_y_coord)
				enemies.remove(i)
				continue
			neg_x_i = self.collision(self.neg_x_bullets,v,enemies.get_size())
			if neg_x_i != -1:
				split_x_coord = self.neg_x_bullets.pop(neg_x_i)
				self.split_x(split_x_coord)
				enemies.remove(i)
				continue
			neg_y_i = self.collision(self.neg_y_bullets,v,enemies.get_size())
			if neg_y_i != -1:
				split_y_coord = self.neg_y_bullets.pop(neg_y_i)
				self.split_y(split_y_coord)
				enemies.remove(i)
				continue
			
	def collision(self, bullets, enemy, variance):
		for i in range(len(bullets)-1, -1, -1):
			dif_X = bullets[i][0] - enemy[0]
			dif_Y = bullets[i][1] - enemy[1]
			if abs(dif_X) < variance and abs(dif_Y) < variance:
				return i
		return -1
		
	def split_x(self, coordinates):
		self.pos_y_bullets.append([coordinates[0],coordinates[1]])
		self.neg_y_bullets.append([coordinates[0],coordinates[1]])
		
	def split_y(self, coordinates):
		self.pos_x_bullets.append([coordinates[0],coordinates[1]])
		self.neg_x_bullets.append([coordinates[0],coordinates[1]])

	def get_rate(self):
		return self.rate
		
	def set_rate(self, value):
		self.rate = value

	def set_size(self, amount):
		self.size = 2
	
	def get_size(self):
		return self.size
	
	def increment(self):
		for v in self.pos_x_bullets:
			v[0] += self.distance
		for v in self.pos_y_bullets:
			v[1] += self.distance
		for v in self.neg_x_bullets:
			v[0] -= self.distance
		for v in self.neg_y_bullets:
			v[1] -= self.distance

	def get(self):
		self.increment()
		all_bullets = []
		if len(self.pos_x_bullets):
			all_bullets.extend(self.pos_x_bullets)
		if len(self.pos_y_bullets):
			all_bullets.extend(self.pos_y_bullets)
		if len(self.neg_x_bullets):
			all_bullets.extend(self.neg_x_bullets)
		if len(self.neg_y_bullets):
			all_bullets.extend(self.neg_y_bullets)
		return all_bullets
	
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
	
class Enemies:
	def __init__(self):
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
	
	def is_empty(self):
		if len(self.enemies):
			return False
		return True
		
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
						self.bullets.shoot(self.fighter.get())
			screen.fill([0,0,0])
			self.bullets.impact(self.enemies)
			for bullet in self.bullets.get():
				pygame.draw.circle(screen,self.bullets.get_color(),bullet,self.bullets.get_size())
			for enemy in self.enemies.get():
				pygame.draw.circle(screen, [255,0,0], enemy, self.enemies.get_size())
			self.fighter.set(pygame.mouse.get_pos())
			pygame.draw.polygon(screen,[255,255,255], self.fighter.get_coords())
			pygame.mouse.set_visible(False)
			pygame.display.flip()
			clock.tick(100)
		pygame.quit()

Game = MousePilot()
Game.main_loop()