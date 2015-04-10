import random, pygame

class GameText:
	def __init__(self, screen):
		self.window_size = [600,600]
		self.color = [255,255,255]
		self.screen = screen
	
	def set_window_size(self,x,y):
		self.window_size = [x,y]
	
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
		
	def continue_screen(self,color,option=0):
		font = pygame.font.SysFont("monotype", 20, bold=True)
		text = "Game Paused"
		pause_menu = font.render(text, 1, color)
		
		#Get the center 
		x = self.center_x(text,font,self.window_size)
		y = self.center_y(text,font,self.window_size)
		
		#Set a different color for the hovered options
		colors = [color,color]
		colors[option] = [255-color[0],255-color[1],255-color[2]]
		font2 = pygame.font.SysFont("monotype", 15, bold=False)
		option_txt = ["Resume","Quit"]
		option = [font.render(option_txt[0], 1, color[0]),
					font.render(option_txt[1], 1, color[1])]
		
		#Draw items on the screen
		self.screen.blit(pause_menu,[x/2,y])
		self.screen.blit(option[0], [x,y])
		self.screen.blit(option[1], [3 * x/2,y])	
	
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
