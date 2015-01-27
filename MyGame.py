import pygame, random, time
	
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

	def bullet(self,coordinates):
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
		hits = 0
		enemy = enemies.get()
		for i in range(len(enemy)-1,-1,-1):
			enemy[i].get()
			for bullet in self.bullets:
				if bullet.impact(enemy[i].get_coord(),enemy[i].get_size()):
					enemies.remove(i)
					hits += 1
					break
		return hits
	
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
			if self.bullets[i].redraw(screen):
				continue
			else:
				del self.bullets[i]
	
	def reset(self):
		self.bullets = []
	
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
			y = random.randrange(-3000, -50)
			enemy = Enemy([x,y])
			enemy.set_color([random.randrange(100,255),random.randrange(0,255),random.randrange(0,255)])
			enemy.set_rate(random.randrange(1,4))
			enemy.set_size(random.randrange(4,10) * 2)
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
 
class GameText:
	def __init__(self, screen):
		self.window_size = [600,600]
		self.color = [255,255,255]
		self.screen = screen
	
	def upper_left(self,text='',font='',window_size=[0,0]):
		return [0,0]
		
	def upper_right(self,text,font,window_size):
		size = font.size(text)
		x = window_size[0] - size[0]
		return [x,0]
		
	def lower_left(self,text,font,window_size):
		size = font.size(text)
		y = window_size[1] - size[1]
		return [0,y]
		
	def lower_right(self,text,font,window_size):
		size = font.size(text)
		x = window_size[0] - size[0]
		y = window_size[1] - size[1]
		return [x,y]
	
	def center_x(self,text,font,window_size):
		size = font.size(text)
		x = (window_size[0] - size[0]) / 2
		return x
	
	def center_y(self,text,font,window_size):
		size = font.size(text)
		y = (window_size[1] - size[1]) / 2
		return y
		
	def center(self,text,font,window_size):
		x = self.center_x(text,font,window_size)
		y = self.center_y(text,font,window_size)
		return [x,y]
	
	def title_text(self, color):
		font = pygame.font.SysFont("monotype", 100, bold=True)
		text = "CATALYST"
		title = font.render(text, 1, color)
		xy = self.center(text,font,self.window_size)
		self.screen.blit(title,xy)
	
	def start_text(self, color):
		font = pygame.font.SysFont("monotype", 30, bold=True)
		text = "Press 'SPACE' to start"
		title = font.render(text, 1, color)
		x = self.center_x(text,font,self.window_size)
		y = 2 * self.window_size[1] / 3
		self.screen.blit(title,[x,y])

	def press_any_button_text(self, color): 
		font = pygame.font.SysFont("monotype", 20, bold=True)
		text = "Press 'SPACE' to continue"
		pressany = font.render(text, 1, color)
		x = self.center_x(text,font,self.window_size)
		y = 2 * self.window_size[1]/3
		self.screen.blit(pressany,[x,y])
		
	def continue_screen(self):
		pass
		
	def gameover_text(self, color):
		font = pygame.font.SysFont("monotype", 70, bold=True)
		text = "Game Over"
		gameover = font.render(text, 1, color)
		x = self.center_x(text,font,self.window_size)
		y = self.window_size[1]/3
		self.screen.blit(gameover,[x,y])
		
	def display_score(self, score, color):
		font = pygame.font.SysFont("monotype", 30, bold=True)
		text = str(score)
		xy = self.upper_right(text,font,self.window_size)
		score_text = font.render(text, 1, color)
		self.screen.blit(score_text,xy)
		
	def get_color(self):
		return self.color
		
	def set_color(self, color):
		self.color = color
	
	def level_text(self,level):
		color = []
		color.append(random.randrange(130,255))
		color.append(random.randrange(130,255))
		color.append(random.randrange(130,255))
		font = pygame.font.SysFont("monotype", 75, bold=True)
		text = "Level " + str(level)
		xy = self.center(text,font,self.window_size)
		level_up = font.render(text,1,color)
		self.screen.blit(level_up,xy)
	
class Game:
	def __init__(self):
		self.fighter = Fighter()
		self.enemies = Enemies()
		self.bullets = Bullets()
		self.level = 1
		self.shoot_rate = self.bullets.get_rate()
		self.enemies_created = 1000
		self.enemies.set_amount(self.enemies_created)
		self.window_size = [600, 600]
		self.screen = pygame.display.set_mode(self.window_size,16)
		self.reset_screen = self.screen
		pygame.display.set_caption("")
		self.text = GameText(self.screen)
		pygame.init()
		self.clock = pygame.time.Clock()
		
	def level_up(self):
		self.enemies_created += self.enemies_created / 5
		self.enemies.set_amount(self.enemies_created)
		self.shoot_rate += self.shoot_rate * .3
		self.bullets.set_rate(self.shoot_rate)
		self.level += 1
		self.text.level_text(self.level)
		pygame.display.flip()
		time.sleep(1)
		
	def reset(self):
		self.enemies_created = 100
		self.screen = self.reset_screen
		self.enemies.set_amount(self.enemies_created)
		self.shoot_rate = .2
		self.game_over = 0
		self.score = 0
		self.bullets.set_rate(self.shoot_rate)
		self.bullets.reset()
		self.level = 1

	def main_loop(self):
		self.reset()
		done = False
		pygame.key.set_repeat(1,1)
		total_hits = 0
		while not done and not self.game_over:
			if self.score > 1 and self.score % 5000 == 0:
				self.level_up()
			elif self.score < 0:
				self.gameover()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					done = True
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_b or event.type == pygame.MOUSEBUTTONDOWN:
			 			self.bullets.bullet(self.fighter.get())
					if event.key == pygame.K_v:
						self.bullets.catalyst(self.fighter.get())
					if event.key == pygame.K_c:
						self.bullets.explosive(self.fighter.get())
			self.screen.fill([0,0,0])
			total_hits = self.bullets.get_hits(self.enemies)
			self.score -= total_hits * 100
			self.bullets.redraw(self.screen)
			self.fighter.set(pygame.mouse.get_pos())
			for enemy in self.enemies.get():
				if self.fighter.hit(enemy.get_coord(),enemy.get_size()):
					self.game_over = 1
				enemy.redraw(self.screen)
			pygame.draw.polygon(self.screen,self.fighter.get_color(), self.fighter.get_coords())
			self.text.display_score(self.score,[255,255,255])
			pygame.mouse.set_visible(False)
			pygame.display.flip()
			self.last_surface = self.screen.copy()
			self.score += 5
			self.clock.tick(100)
		if self.game_over:
			
			self.gameover()
		else:
			pygame.quit()
		
	def gameover(self):
		done = False
		quit = False
		colors = [[255,0,0],[0,255,0],[0,0,255],[255,255,0]]
		i = 0
		while not done and not quit:
			self.screen.fill([0,0,0])
			self.screen.blit(self.last_surface,[0,0])
			if i < 3:
				i += 1
				if i % 2 == 1:
					self.text.press_any_button_text([255,255,255])
			else: 
				i = 0	
			self.text.gameover_text(colors[i])
			pygame.mouse.set_visible(True)
			pygame.display.flip()
			self.clock.tick(2)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					quit = True
					break
				elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
					if event.key == pygame.K_SPACE:
						done = True
						break
					elif event.key == pygame.K_ESCAPE:
						quit = True
						break
		if done:
			self.main_loop()
		else:
			self.start_screen()
	
	def start_screen(self):
		self.reset()
		ready = 0
		quit = 0
		i = 0
		while not ready and not quit:
			self.screen.fill([0,0,0])
			i += 1
			if i % 2 == 1: 
				self.text.start_text([255,255,255])
				i = -1
			self.text.title_text([55,255,55])
			pygame.mouse.set_visible(True)
			pygame.display.flip()
			self.clock.tick(2)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					quit = True
					break
				elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
					if event.key == pygame.K_SPACE:
						ready = True
						break
					elif event.key == pygame.K_ESCAPE:
						quit = True
						break
		if ready:
			self.main_loop()
		else:
			pygame.quit()
	
Game = Game()
Game.start_screen()