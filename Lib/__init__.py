import pygame,time
from pygame.locals import *
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
		self.screen = pygame.display.set_mode(self.window_size,HWSURFACE|DOUBLEBUF|RESIZABLE)
		self.reset_screen = self.screen
		pygame.display.set_caption("")
		self.text = GameText(self.screen)
		pygame.init()
		self.clock = pygame.time.Clock()
	
	def level_up(self):
		'''Level up and alter elements in the game accordingly'''
		self.enemies_created += self.enemies_created / 5
		self.enemies.set_amount(self.enemies_created)
		self.shoot_rate += self.shoot_rate * .3
		self.bullets.set_rate(self.shoot_rate)
		self.level += 1
		self.text.level_text(self.level)
		pygame.display.flip()
		time.sleep(1)
		
	def reset(self):
		'''Reset the game'''
		self.enemies_created = 100
		self.screen = self.reset_screen
		self.enemies.set_amount(self.enemies_created)
		self.shoot_rate = .2
		self.score,self.game_over = [0,0]
		self.bullets.set_rate(self.shoot_rate)
		self.bullets.reset()
		self.level = 1

	def resize(self,event):
		'''Resize the inner window elements'''
		self.window_size = [event.w,event.h]
		screen = pygame.display.set_mode(self.window_size,HWSURFACE|DOUBLEBUF|RESIZABLE)
		self.bullets.set_window_size(self.window_size[0],self.window_size[1])
		self.enemies.set_window_size(self.window_size[0],self.window_size[1])
		self.text.set_window_size(self.window_size[0],self.window_size[1])
		pygame.display.flip()
		
	def main_loop(self):
		self.reset()
		[exit,self.game_over,total_hits] = [False,False,0]
		pygame.key.set_repeat(1,1)
		while True not in [exit,self.game_over]:
		
			#Score is high enough to increase a level
			if self.score > 1 and self.score % (self.level * 5000) == 0:
				self.level_up()
				
			#Score has dropped below the threshhold for the current level, player looses
			elif self.score < (self.level - 1) * 5000:
				self.game_over = True
				break
			
			#Event evaulation loop
			for event in pygame.event.get():
				#If player hit 'X' on window, end the game 
				if event.type == pygame.QUIT:
					exit = True
					break
					
				#If the event is a window resizing, resize the inner elements as well
				elif event.type == VIDEORESIZE:
					self.resize(event)
					
				#Key/Mouse events
				elif event.type == pygame.KEYDOWN:
					#Regular bullets shoot when 'B' or a mouse button is clicked
					if event.key == pygame.K_b or event.type == pygame.MOUSEBUTTONDOWN:
			 			self.bullets.bullet(self.fighter.get())
						
					#Catalyst bullets shoot when 'V' is pressed
					elif event.key == pygame.K_v:
						self.bullets.catalyst(self.fighter.get())
						
					#Explosive bullets shoot when 'C' is pressed
					elif event.key == pygame.K_c:
						self.bullets.explosive(self.fighter.get())
						
					#Switch to next song when 'X' is pressed
					elif event.key == pygame.K_x:
						self.music.next()
						
					#Mute the song when 'M' is pressed
					elif event.key == pygame.K_m:
						self.music.mute()
						
					#Go to pause menu loop if 'ESC' is pressed
					elif event.key == pygame.K_ESCAPE:
						self.pause_screen()
						
			#Draw a black background over the screen
			self.screen.fill([0,0,0])
			
			#Get the total hits by bullets on the enemies
			total_hits = self.bullets.get_hits(self.enemies)
			
			#Subtract of the total hits off the current running score
			self.score -= total_hits * 100
			
			#Redraw the bullets, set the fighter, and calculate/redraw the enemies
			self.bullets.redraw(self.screen)
			self.fighter.set(pygame.mouse.get_pos())
			
			#loop through the enemy list in reverse so they can be deleted on-the-fly if need be
			index = self.enemies.last_index()
			for enemy in reversed(self.enemies.get()):
				#If fighter coordinates overlapped with enemy, the enemy dies.
				if self.fighter.hit(enemy.get_coord(),enemy.get_size()):
					self.score -= 1000
					#enemy destroyed, Remove the enemy. 
					self.enemies.remove(index)
				#Otherwise, redraw that enemy on the screen
				else:
					enemy.redraw(self.screen)
				#Decrement index
				index -= 1
					
			#Draw the fighter on the screen, update the score text, and flip the display (draws the new items)
			pygame.draw.polygon(self.screen,self.fighter.get_color(), self.fighter.get_coords())
			self.text.display_score(self.score,[255,255,255])
			pygame.mouse.set_visible(False)
			pygame.display.flip()
			
			#Store the current surface
			self.last_surface = self.screen.copy()
			
			#Add to the current running score
			self.score += 5
			
			#Timer for when to repeat the loop
			self.clock.tick(1000)
			
		#Loop ended due to game over
		if self.game_over:
			self.gameover()
		#Loop ended due to player closing game
		else:
			pygame.quit()
	
	def event_handler(self,event,phase):
		#return in form of [ready,quit]
		if phase in ["start","gameover"]:
			if event.type == pygame.QUIT:
					return [False,True]
			elif event.type == VIDEORESIZE:
				self.resize(event)
			elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
				if event.key == pygame.K_SPACE:
					return [True,False]
				elif event.key == pygame.K_ESCAPE:
					return [False,True]
				elif event.key == pygame.K_m:
					self.music.mute()
				elif event.key == pygame.K_x:
					self.music.next()
			return [False,False]
			
		#returns in form of [ready,quit,j]
		elif phase == "pause":
			if event.type == pygame.QUIT:
				return [False,True,0]
			elif event.type == VIDEORESIZE:
				self.resize(event)
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_DOWN:
					return [False,False,1]
				elif event.key == pygame.K_UP:
					return [False,False,-1]
				elif event.key == pygame.K_RETURN:
					return [True,True,0]
			return [False,False,0]
					
	def gameover(self):
		ready,quit,i = [False,False,0]
		colors = [[255,0,0],[0,255,0],[0,0,255],[255,255,0]]
		pygame.mouse.set_visible(True)
		while True not in [ready, quit]:
			self.screen.fill([0,0,0])
			#Use the moment of game over screen as background
			self.screen.blit(self.last_surface,[0,0])
			#variable i is used to cause a rotation of colors and blinking effects on text
			if i < 3:
				i += 1
				if i % 2 == 1:
					self.text.press_any_button_text([255,255,255])
			else: 
				i = 0	
			self.text.gameover_text(colors[i])
			
			#Event loop
			for event in pygame.event.get():
				#Call the event handler
				[ready,quit] = self.event_handler(event,"gameover")
				if ready or quit:
					break
				
			#Draw the new screen
			pygame.display.flip()
			#sleep timer before looping again
			self.clock.tick(2)	
		
		if ready:
			self.main_loop()
		else:
			self.start_screen()
	
	def start_screen(self):
		ready,quit,i = [False,False,0]
		
		#Reset game elements
		self.reset()
		pygame.mouse.set_visible(True)
		
		#start screen loop
		while True not in [ready, quit]:
			self.screen.fill([0,0,0])
			#variable i is used to cause a blinking effect on the text
			i += 1
			if i % 2 == 1: 
				self.text.start_text([255,255,255])
				i = -1
			self.text.title_text([55,255,55])
			
			#Event loop
			for event in pygame.event.get():
				[ready,quit] = self.event_handler(event,"start")
				if ready or quit:
					break
			
			#refresh the screen
			pygame.display.flip()
			
			#sleep timer for loop
			self.clock.tick(2)
			
		if ready:
			self.main_loop()
		else:
			pygame.quit()
	
	def pause_screen(self):
		ready,quit,i,j = [False,False,0,0]
		while True not in [ready,quit]:
			self.screen.fill([0,0,0])
			self.text.continue_screen([55,255,55],i)
			pygame.display.flip()
			self.clock.tick(10)
			for event in pygame.event.get():
				[ready,quit,j] = self.event_handler(event,"pause")
				if ready and quit: 
					if i: ready = False
					else: quit = False
				i += j
				if i < 0: i = 1
				elif i > 1: i = 0
		if quit:
			self.start_screen()
		
