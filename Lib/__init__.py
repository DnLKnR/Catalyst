import pygame,time
from Lib.fighter import Fighter
from Lib.enemies import Enemies
from Lib.bullets import Bullets
from Lib.text import GameText
from Lib.sound import Sound

class Main:
	def __init__(self):
		self.fighter = Fighter()
		self.enemies = Enemies()
		self.bullets = Bullets()
		self.music = Sound()
		self.music.play()
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
				if event.type == VIDEORESIZE:
					self.window_size = event.dict['size']
					print(self.window_size)
					screen=pygame.display.set_mode(self.window_size,HWSURFACE|DOUBLEBUF|RESIZABLE)
					pygame.display.flip()
					self.bullets.set_window_size(self.window_size[0],self.window_size[1])
					self.enemies.set_window_size(self.window_size[0],self.window_size[1])
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_b or event.type == pygame.MOUSEBUTTONDOWN:
			 			self.bullets.bullet(self.fighter.get())
					if event.key == pygame.K_v:
						self.bullets.catalyst(self.fighter.get())
					if event.key == pygame.K_c:
						self.bullets.explosive(self.fighter.get())
					if event.key == pygame.K_x:
						self.music.next()
					if event.key == pygame.K_m:
						self.music.mute()
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
			self.clock.tick(1000)
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
					if event.key == pygame.K_m:
						self.music.mute()
					if event.key == pygame.K_x:
						self.music.next()
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
					if event.key == pygame.K_ESCAPE:
						quit = True
						break
					if event.key == pygame.K_x:
						self.music.next()
					if event.key == pygame.K_m:
						self.music.mute()
		if ready:
			self.main_loop()
		else:
			pygame.quit()
