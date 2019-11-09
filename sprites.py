import pygame
vec = pygame.math.Vector2
import random


TITLE = "Carrots"
WIDTH = 480
HEIGHT = 600
FPS = 60
PLAYER_FRICTION = -0.12
PLAYER_GRAVITY = 0.8
SPRITESHEET = "spritesheet_jumper.png"


# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 255)
YELLOW =(255,255,0)

class SpriteSheet:
	def __init__(self,filename):
		self.spritesheet = pygame.image.load(filename).convert()
		
		
	def get_image(self,x,y,width,height):
		image = pygame.Surface((width,height))
		image.blit(self.spritesheet,(0,0),(x,y,width,height))
		image = pygame.transform.scale(image,(width// 2,height // 2))
		return image
		
		
	

class Player(pygame.sprite.Sprite):
	def __init__(self,game):
		self._layer=2
		self.game = game
		pygame.sprite.Sprite.__init__(self)
		self.image=self.game.spritesheet.get_image(614,1063,120,191)
		self.image.set_colorkey(BLACK)
		#self.image.fill(YELLOW)
		self.rect=self.image.get_rect()
		self.rect.center=(WIDTH/2,HEIGHT/2)
		self.pos = vec(WIDTH/2,HEIGHT/2)
		self.vel=vec(0, 0)
		self.acc=vec(0, 0)
		
		
		self.vx=0
		self.vy=0
		
	def jump(self):
		self.rect.x += 1
		hits = pygame.sprite.spritecollide(self, self.game.platform,False)
		self.rect.x -= 1
		
		self.vel.y = -15
		
	def update(self):
		self.acc=vec(0, 0.5)
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			self.acc.x = -0.9
		if keys[pygame.K_RIGHT]:
			self.acc.x = 0.9
			
		#self.rect.x += self.vx
		#self.rect.y += self.vy
		
		self.acc.x += self.vel.x * PLAYER_FRICTION
		self.vel += self.acc
		self.pos += self.vel + 0.5*self.acc
		
		if self.pos.x > WIDTH:
			self.pos.x = 0
		if self.pos.x < 0:
			self.pos.x = WIDTH

		
		self.rect.midbottom = self.pos
		
		def animate(self):
			now = pygame.time.get_ticks()
			if self.vel.x!=0:
				self.walking = True
			else:
				self.walking = False
			
				
			
		
#class Powerups()
		
		
class Platforms(pygame.sprite.Sprite):
	def __init__(self,game,x,y):
		self._layer=1
		pygame.sprite.Sprite.__init__(self)
		self.game = game
		images=[ self.game.spritesheet.get_image(0,288,380,94),self.game.spritesheet.get_image(0,288,380,94),self.game.spritesheet.get_image(213,1662,201,100)]
		for i in range(2):
			self.image=images[i]
			self.image.set_colorkey(BLACK)
		#self.image.fill(GREEN)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y
		


class Enemies(pygame.sprite.Sprite):
	def __init__(self,game):
		self._layer=3
		pygame.sprite.Sprite.__init__(self)
		self.game = game
		self.image=self.game.spritesheet.get_image(820,1733,78,70)
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH-self.rect.width)
		self.rect.y = -600
		self.vy = 6
		self.vy += 1
		self.vx = 0
		
	def update(self):
		self.rect.y += self.vy
		if self.rect.top>HEIGHT+10:
			self.rect.x = random.randrange(WIDTH-self.rect.width)
			self.rect.y = -600
			self.vy +=1
			
class Carrots(pygame.sprite.Sprite):
	def __init__(self,game):
		self._layer=4
		pygame.sprite.Sprite.__init__(self)
		self.game = game
		self.image = pygame.Surface((30,30))
		self.image.fill(GREEN)
		self.rect = self.image.get_rect()
		self.rect.x = random.randrange(WIDTH-self.rect.width)
		self.rect.y = -600
		self.vy = 0
		self.vx = 0
		
	def update(self):
		self.rect.y += self.vy
		if self.rect.top>HEIGHT+10:
			self.rect.x = random.randrange(WIDTH-self.rect.width*2)
			self.rect.y = -100
			self.vy +=1
		

		

#	
