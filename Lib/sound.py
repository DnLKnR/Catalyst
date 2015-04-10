import os, pygame


class Sound:
	def __init__(self):
		pygame.mixer.init()
		self.music = []
		self.is_mute = 0
		self.timer = 0
		self.index = 0
		loaded = []
		maindir = os.getcwd().replace('\\','/')
		maindir += '/Lib/Music/'
		for file in os.listdir(maindir):
			if '.wav' in file or '.mp3' in file:
				if file in loaded:
					continue
				loaded.append(file)
				self.music.append(pygame.mixer.Sound('Lib/Music/' + file))
		
	def play(self):
		if len(self.music):
			self.music[self.index].play(-1,0,1000)
			self.timer = time.time()
	
	def next(self):
		if not self.is_empty() and abs(self.timer - time.time()) > 1:
			self.stop()
			self.index += 1
			if self.index == len(self.music):
				self.index = 0
			self.play()
			self.timer = time.time()
	
	def stop(self):
		self.music[self.index].stop()
	
	def mute(self):
		if not self.is_empty() and abs(self.timer - time.time()) > 1:
			self.timer = time.time()
			if self.is_mute:
				self.is_mute = 0
				self.music[self.index].set_volume(1.0)
			else:
				self.is_mute = 1
				self.music[self.index].set_volume(0.0)
	
	def is_empty(self):
		if len(self.music): return False
		else: return True
	
