import pygame
import pygame_menu
from kings__chesss import *

class input_box(object):
	def __init__(self, size, pos, font_size, text=""):
		self.size=size
		self.pos=pos
		self.font_size=font_size
		self.text=text
		self.font = pygame.font.SysFont("arial", self.font_size)
		self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
		self.status=0
	
	def draw(self, win):
		txt = self.font.render(self.text, True, (0, 0, 0))
		if self.status==0:
			color=(189,189,189)
		else:
			color=(220,220,220)
		pygame.draw.rect(win, color, self.rect)
		win.blit(txt, (self.pos[0], self.pos[1]))

	

def online_menu(win, res, nick):
	font_size = int(win.get_size()[0]/45)
	longest_ip="123.123.123.123"
	font = pygame.font.SysFont("arial", font_size)
	eg_render=font.render(longest_ip, True, (0, 0, 0))
	eg_render=eg_render.get_rect()
	ip_box_size=(eg_render.width, eg_render.height)
	ip_box=input_box(ip_box_size, (15,15), font_size, "0.0.0.0")
	boxes=[ip_box]
	playing=1
	
	while playing:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if ip_box.rect.collidepoint(event.pos):
					ip_box.status=1
				else:
					ip_box.status=0
		for box in boxes:
			box.draw(win)
		pygame.display.update()
	