from Lib.Weapons import *
import time

class Bullets:
	def __init__(self):
		self.bullets = []
		self.rate = 0.1
		self.size = 2
		self.distance = 3
		self.color = [0,255,0]
		self.last_bullet_t = time.time()
		self.window_size = [600,600]

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
	
	def set_window_size(self,x,y):
		self.window_size = [x,y]
		for ammo in self.bullets:
			ammo.set_window_size(x,y)
	
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
			if v[0] > self.window_size[0] or v[1] > self.window_size[1]:
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
