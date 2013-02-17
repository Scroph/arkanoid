import pygame

class Carpet:
	def __init__(self, screen):
		self.scr = screen
		self.img = pygame.image.load('carpet.png')
		self.w = self.img.get_width()
		self.h = self.img.get_height()
		self.x = screen.get_width() / 2 - self.w / 2
		self.y = screen.get_height() - self.h
		self.started = False
	
	def event(self, event):
		if event.key == pygame.K_LEFT:
			self.x -= 8
		elif event.key == pygame.K_RIGHT:
			self.x += 8
		elif event.key == pygame.K_SPACE:
			self.started = True
		
		if self.x >= self.scr.get_width() - self.w:
			self.x = self.scr.get_width() - self.w
		elif self.x <= 0:
			self.x = 0
	
	def draw(self):
		self.scr.blit(self.img, (self.x, self.y))
	

class Ball:
	def __init__(self, screen, carpet):
		self.scr = screen
		self.carpet = carpet
		self.img = pygame.image.load('ball.png')
		self.w = self.img.get_width()
		self.h = self.img.get_height()
		self.x = carpet.x - (carpet.w / 2) - (self.w / 2)
		self.y = carpet.y - self.h - 60
		self.xreverse = True 
		self.yreverse = True
	
	def move(self):
		if not self.carpet.started:
			self.x = self.carpet.x + self.carpet.w / 2 - self.w / 2
			self.y = self.carpet.y - self.carpet.h - 3
			return
			
		if self.x >= self.scr.get_width() - self.w or self.x <= self.w:
			self.xreverse = not self.xreverse
		if self.y <= self.h or (self.y >= self.carpet.y - self.carpet.h and self.carpet.x <= self.x <= self.carpet.x + self.carpet.w):
			self.yreverse = not self.yreverse
		#if self.carpet.img.get_rect().colliderect(self.img.get_rect()):
			#self.yreverse = not self.yreverse
		if self.y >= self.scr.get_height() - self.h:
			if self.x + self.w < self.carpet.x:
				raise GameLost('Ball is out of boundaries')
			elif self.x > self.carpet.x + self.carpet.w:
				raise GameLost('Ball is out of boundaries')
			else:
				self.yreverse = not self.yreverse
		
		if self.xreverse:
			self.x -= 3
		else:
			self.x += 3
		
		if self.yreverse:
			self.y -= 3
		else:
			self.y += 3
	
	def draw(self):
		self.scr.blit(self.img, (self.x, self.y))
		

class Brick:
	def __init__(self, screen, x, y):
		self.x = x
		self.y = y
		self.scr = screen
		self.img = pygame.image.load('brick.png')
		self.w = self.img.get_width()
		self.h = self.img.get_height()
		self.touched = False
	
	def istouched(self, obj):
		if self.touched: #already touched by the ball
			return True
		
		if self.x <= obj.x <= self.x + self.w:
			if self.y <= obj.y <= self.y + self.h:
				obj.yreverse = not obj.yreverse
				self.touched = True
				self.img = pygame.image.load('void.png')
				return True
		
		return False
	
	def draw(self):
		self.scr.blit(self.img, (self.x, self.y))

class BrickSet:
	def __init__(self, screen, xstart = 0, xend = 0, ystart = 0, yend = 0):
		self.bricks = []
		tmp = Brick(screen, 0, 0)
		if xend == 0:
			xend = screen.get_width()
		if yend == 0:
			yend = screen.get_height() / 2
		
		print xstart, xend, ystart, yend
		for x in xrange(xstart, xend, tmp.w):
			for y in xrange(ystart, yend, tmp.h):
				b = Brick(screen, x, y)
				self.bricks.append(b)
	
	def check(self):
		for b in self.bricks:
			if not b.touched:
				return False
		
		return True
	
	def draw(self, ball):
		for b in self.bricks:
			b.istouched(ball)
			b.draw()
	
	def get_bricks(self):
		return self.bricks

class GameLost(Exception):
	def __init__(self, msg):
		Exception(msg)
