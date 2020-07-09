import pygame
import random
import os
import time
pygame.font.init()
pygame.init()

# loading assets
VBAR_IMG = pygame.image.load(os.path.join("imgs","vrec.png"))
HBAR_IMG = pygame.image.load(os.path.join("imgs","hrec.png"))
UNSELECTED_VBAR = pygame.image.load(os.path.join("imgs","vrecSELECTED.png"))
UNSELECTED_HBAR = pygame.image.load(os.path.join("imgs","hrecSELECTED.png"))
WINNER_IMG = pygame.image.load(os.path.join("imgs","winner.png"))
GAMEOVER_IMG = pygame.image.load(os.path.join("imgs","go.png"))
CIR_IMG = pygame.image.load(os.path.join("imgs","cir.png"))

STAT_FONT = pygame.font.SysFont("comicsans",50)

class Bar():
	
	def __init__(self,IMGS,state=False,tilt=0,x=50,y=50):
		self.state = state
		self.IMGS =IMGS
		self.img = IMGS[0] if self.state else IMGS[1] 
		self.x = x
		self.y = y
		self.tilt = tilt
		self.img_rect = self.img.get_rect(center=self.img.get_rect(topleft=(self.x,self.y)).center)

	def assign_bars(self,left,right):
		self.left = left
		self.right = right
		
	def draw(self,win):
		self.img = self.IMGS[0] if self.state else self.IMGS[1]
		win.blit(self.img,self.img_rect.topleft)
		
	def get_mask(self):
		return pygame.mask.from_surface(self.img)

def draw_window(win,bars,bullet,score):

	for bar in bars:
		bar.draw(win)
	text = STAT_FONT.render("Score " +str(score),1,(255,255,255))
	win.blit(text,(WIN_WIDTH-10-text.get_width(),10))
	bullet.draw(win)
	bullet.move()

		
		
		
class Bullet:

	def __init__(self,enter_point,bullet_img,vel=(0,-1),x=290,y=540):
		self.img = bullet_img
		self.vel = vel
		self.x = x
		self.y = y
		self.init_x = x
		self.init_y = y
		self.enter_point = enter_point
		self.hit_box = (x,y,self.img.get_width(),self.img.get_height())

	def re_init(self):
		self.x = self.init_x
		self.y = self.init_y

	def move(self):
		global score
		self.x+=self.vel[0]*(1+(score/(score+3)))
		self.y+=self.vel[1]*(1+(score/(score+3)))
		self.hit_box = (self.x,self.y,self.img.get_width(),self.img.get_height())

	def draw(self,win):
		win.blit(self.img,(self.x,self.y))
	
	def collide(self,win):
		cx , cy = self.x + self.enter_point[0] , self.y + self.enter_point[1]
		if cx > 155 and cx < 465:
			if cy > 185 and cy < 495 :
				return True
		return False

	def collision_bar(self,bar):
		self.collision_bar = bar 
	

pygame.display.set_caption("FOUR SIDES")
WIN_WIDTH = 600
WIN_HEIGHT = 600
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

b1 = Bar(IMGS=[HBAR_IMG,UNSELECTED_HBAR],state=True,tilt=0,x=185,y=185)
b2 = Bar(IMGS=[VBAR_IMG,UNSELECTED_VBAR],state=False,tilt=0,x=b1.x+b1.img.get_width(),y=b1.y+b1.img.get_height())
b3 = Bar(IMGS=[HBAR_IMG,UNSELECTED_HBAR],state=False,tilt=0,x=b1.x,y=b1.y+b1.img.get_height()+b2.img.get_height())
b4 = Bar(IMGS=[VBAR_IMG,UNSELECTED_VBAR],state=False,tilt=0,x=b1.x-b2.img.get_width(),y=b2.y)

# asigning the left and right bars for each bar
b1.assign_bars(b4,b2)
b2.assign_bars(b1,b3)
b3.assign_bars(b2,b4)
b4.assign_bars(b3,b1)

# initializing the 4 bullets
ubullet = Bullet(bullet_img=CIR_IMG,vel=(0,-2),x=285,y=600,enter_point=(0,0))
dbullet = Bullet(bullet_img=CIR_IMG,vel=(0,2),x=285,y=-30,enter_point=(0,30))
lbullet = Bullet(bullet_img=CIR_IMG,vel=(-2,0),x=600,y=285,enter_point=(0,0))
rbullet = Bullet(bullet_img=CIR_IMG,vel=(2,0),x=-30,y=285,enter_point=(30,0))

# allocating the bullet collision check bar
ubullet.collision_bar(b3)
dbullet.collision_bar(b1)
lbullet.collision_bar(b2)
rbullet.collision_bar(b4)

bullet_list = [ubullet,dbullet,lbullet,rbullet]
bullet=random.choice(bullet_list)

# initialisation for the game
bars = [b1,b2,b3,b4]
clock = pygame.time.Clock()
run = True
inGame = True
click = -1
lost = False
point = False
winner = False
score = 0
while run:
	clock.tick(30)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
	if inGame:
		# click is used to know if respond to input or not (-ve means waiting for input , +ve means not listening for input) 
		if click < 0:
			keys = pygame.key.get_pressed()
			for b in bars:
				if b.state==True:
					active_bar = b
					break
			
			if keys[pygame.K_LEFT]:
				active_bar.state=False
				active_bar.left.state=True
				click = 5
			elif keys[pygame.K_RIGHT]:
				active_bar.state=False
				active_bar.right.state=True
				click = 5
		click-=1

		if bullet.collide(WIN):
			if bullet.collision_bar.state==True:
				point = True
			else:
				lost = True
				inGame = False
		
		if point:
			score+=1
			bullet.re_init()
			bullet=random.choice(bullet_list)
			point = False
			
		if score>=10:
			winner = True
			inGame = False
		
		WIN.fill((0,0,0))
		draw_window(WIN,bars,bullet,score)
		
	else:
		if winner==True:
			bullet.re_init()
			WIN.fill((50,50,50))
			WIN.blit(WINNER_IMG,(200,200))
		if lost==True:
			bullet.re_init()
			WIN.fill((50,50,50))
			WIN.blit(GAMEOVER_IMG,(0,100))
	text = STAT_FONT.render("Score " +str(score),1,(255,255,255))
	WIN.blit(text,(WIN_WIDTH-10-text.get_width(),10))
	pygame.display.update()
pygame.quit()