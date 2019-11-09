import pygame
import random
import time
from sprites import *
from os import path

TITLE = "Carrots"
WIDTH = 480
HEIGHT = 600
FPS = 60
FONT_NAME = 'arial'

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (128, 255, 0)
BLUE = (0, 255, 255)
YELLOW = (255,255,0)
ORANGE = ( 230, 126,34)
DARKBLUE =(52, 152, 219)
SPRITESHEET = "spritesheet_jumper.png"
HIGH_SCORE="highscore.txt"
PLATFORMLIST = [(0,HEIGHT-60),(190,HEIGHT-60),(380,HEIGHT-60)]

class Game:
	def __init__(self):
		pygame.init()
		pygame.mixer.init()
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		pygame.display.set_caption("My Game")
		self.clock = pygame.time.Clock()
		self.running = True
		self.font_name = pygame.font.match_font(FONT_NAME)
		self.load_data()
		
	def load_data(self):
		self.dir = path.dirname(__file__)
		
		image_dir = path.join(self.dir,'pics')
		
		self.spritesheet = SpriteSheet(path.join(image_dir,SPRITESHEET))
		with open(path.join(self.dir, HIGH_SCORE), 'r') as f:
			self.highscore = int(f.read())
   
	def new(self):
		#startnewgame
		self.score = 0
		self.timer = 0
		self.timerrate = 15
		self.all_sprites = pygame.sprite.Group()
		self.enemies = pygame.sprite.Group()
		for i in range(6):
			self.e = Enemies(self)
			self.all_sprites.add(self.e)
			self.enemies.add(self.e)
		
		self.corrots = pygame.sprite.Group()
		self.cart = Carrots(self)
		self.all_sprites.add(self.cart)
		self.corrots.add(self.cart)
		
		
		self.platform = pygame.sprite.Group()
		self.player=Player(self)
		self.all_sprites.add(self.player)
		
		for plat in PLATFORMLIST:
			p = Platforms(self,*plat)
		
			self.all_sprites.add(p)
			self.platform.add(p)
		self.run()
		
		
		
	def run(self):
		#game loop
		
		self.playing = True
		while self.playing:
			self.clock.tick(FPS)
			self.events()
			self.update()
			self.draw()
		
		
	def update(self):
		self.all_sprites.update()
		hits = pygame.sprite.spritecollide(self.player,self.platform,False)
		if hits:
			self.player.pos.y = hits[0].rect.top
			self.player.vel.y = 0
		self.timer -=1
		if self.timer%60 == 0:
			self.timerrate -= 1	
		Enemies(self)
		cold = pygame.sprite.spritecollide(self.player,self.enemies,True)
		if cold:
			self.score += 1
			self.e = Enemies(self)
			self.all_sprites.add(self.e)
			self.enemies.add(self.e)
			
		if self.timerrate == 0:
			self.playing = False
		
	def events(self):
		for event in pygame.event.get():
		    # check for closing window
			if event.type == pygame.QUIT:
				if self.playing:
					self.playing = False
				self.running = False
		        
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					self.player.jump()

		
		
	def draw(self):
		self.screen.fill(BLUE)
		self.all_sprites.draw(self.screen)
		self.draw_text("Score: "+str(self.score),22,BLACK,50,15)
		self.draw_text("Time: "+str(self.timerrate),22,BLACK,49,40)
		self.draw_text("Highscore: "+str(self.highscore),22,BLACK,WIDTH-70,15)
		
		if self.timerrate == -1:
			self.draw_text("Time Up!",44,BLACK,WIDTH/2,HEIGHT/2)
		pygame.display.flip()
		
		
	def show_start_screen(self):
        # game splash/start screen
		self.screen.fill(BLUE)
		self.draw_text(TITLE, 100, ORANGE, WIDTH / 2, HEIGHT / 4)
		self.draw_text("Arrows to move, Space to jump", 22, BLACK, WIDTH / 2, HEIGHT / 2)
		pygame.display.flip()
		time.sleep(3)
		

	def show_go_screen(self):
		time.sleep(1)
    
		if not self.running:
			return
		self.screen.fill(BLUE)
		time.sleep(2)
		self.draw_text("GAME OVER", 48, ORANGE, WIDTH / 2, HEIGHT / 4)
		self.draw_text("Score: " + str(self.score), 22, BLACK, WIDTH / 2, HEIGHT / 2)
		self.draw_text("Press Shift key to play again", 22, BLACK, WIDTH / 2, HEIGHT * 3 / 4)
		if self.score > self.highscore:
			self.highscore = self.score
			self.draw_text("NEW HIGH SCORE!", 22, GREEN, WIDTH / 2, HEIGHT / 2 + 40)
			with open(path.join(self.dir, HIGH_SCORE), 'w') as f:
				f.write(str(self.score))
		else:
			self.draw_text("High Score: " + str(self.highscore), 22, BLACK, WIDTH / 2, HEIGHT / 2 + 40)
		pygame.display.flip()
		self.wait_for_key()

	def wait_for_key(self):
		waiting = True
		while waiting:
			self.clock.tick(FPS)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					waiting = False
					self.running = False
#				if event.type == pygame.KEYUP:
#					waiting = False
					
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
						waiting = False
				
		
	def draw_text(self,text,size,color,x,y):
		font = pygame.font.Font(self.font_name,size)
		text_surface = font.render(text,True,color)
		text_rect = text_surface.get_rect()
		text_rect.midtop = (x,y)
		self.screen.blit(text_surface,text_rect)
		
		
g=Game()
g.show_start_screen()
while g.running:
	g.new()
	g.show_go_screen()
pygame.quit
		
		
	
		
