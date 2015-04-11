import pygame



def draw_circle_in_circle(screen, color, coordinates, width):
	pygame.draw.circle(screen, color, coordinates, width)
	negative_color = [255 - color[0], 255 - color[1], 255 - color[2]]
	pygame.draw.circle(screen, negative_color, coordinates, width//2)

def draw_saucer_with_cannon(screen, color, coordinates, length, width):
	end_coordinates = [coordinates[0]-1,coordinates[1]-length]
	pygame.draw.line(screen, [0,255,0], coordinates, end_coordinates, width//2)
	draw_circle_in_circle(screen, color, coordinates, width)


pygame.init()
screen = pygame.display.set_mode([300,300])
pygame.display.set_caption("Object Sampler")
clock = pygame.time.Clock()
done = False
pygame.key.set_repeat(1,1)
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
	screen.fill([0,0,0])
	
	#This gets mouse coordinates (x,y)
	mouse = pygame.mouse.get_pos()
	draw_saucer_with_cannon(screen, [100,0,255], mouse, 30,20)

	pygame.mouse.set_visible(False)
	pygame.display.flip()
	clock.tick(100)
pygame.quit()