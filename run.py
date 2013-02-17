import pygame
import sys
import logic


screen = pygame.display.set_mode((320, 240))
clock = pygame.time.Clock()
carpet = logic.Carpet(screen)
ball = logic.Ball(screen, carpet)
bricks = logic.BrickSet(screen, 30, 270, 30)

score = 0

while True:
	screen.fill((0, 0, 0))
	if bricks.check():
		print 'Game won !'
		break
	
	try:
		carpet.draw()
		ball.move()
		bricks.draw(ball)
		ball.draw()
	except logic.GameLost, e:
		print str(e)
		sys.exit(0)
	
	for event in pygame.event.get():
		if hasattr(event, 'key'):
			if event.key == pygame.K_ESCAPE:
				sys.exit(0)
				break
			else:
				carpet.event(event)
	
	clock.tick(30)
	pygame.display.flip()
	

raw_input('Press a key to quit.')