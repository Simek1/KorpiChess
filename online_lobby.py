import pygame
import pygame_menu
from kings_chess import *

class input_box(object):
	def __init__(self, size, pos, font_size, limit, text="", uppertext=""):
		self.size=size
		self.pos=pos
		self.font_size=font_size
		self.text=text
		self.limit=limit
		self.font = pygame.font.SysFont("arial", self.font_size)
		self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
		self.uppertext=uppertext
		self.status=0
	def draw(self, win):
		txt = self.font.render(self.text, True, (0, 0, 0))
		if self.status==0:
			color=(189,189,189)
		else:
			color=(220,220,220)
		pygame.draw.rect(win, color, self.rect)
		win.blit(txt, (self.pos[0], self.pos[1]))
		if self.uppertext!="":
			txt=self.font.render(self.uppertext, True, (0, 0, 0))
			width=txt.get_rect().width
			win.blit(txt, (self.pos[0]-5-width, self.pos[1]))
	

def online_menu(win, res, nick):
	font_size = int(win.get_size()[0]/45)
	longest_ip="123.123.123.123"
	font = pygame.font.SysFont("arial", font_size)
	eg_render=font.render(longest_ip, True, (0, 0, 0))
	eg_render=eg_render.get_rect()
	ip_box_size=(eg_render.width, eg_render.height)
	join_ip_box=input_box(ip_box_size, ((res[0]/4)-(ip_box_size[0]/2),(res[1]/10)*3), font_size, 15,"", "IP serwera")
	join_port_box=input_box(ip_box_size, ((res[0]/4)-(ip_box_size[0]/2),(res[1]/10)*4), font_size, 8,"", "Port serwera")
	create_ip_box=input_box(ip_box_size, ((res[0]/4)*3-(ip_box_size[0]/2),(res[1]/10)*3), font_size, 15,"0.0.0.0", "IP serwera")
	create_port_box=input_box(ip_box_size, ((res[0]/4)*3-(ip_box_size[0]/2),(res[1]/10)*4), font_size, 8,"", "Port serwera")
	boxes=[join_ip_box, join_port_box, create_ip_box, create_port_box]
	left_column=pygame.Rect(res[0]/40, 0, (res[0]/2)-((res[0]/40)*2), res[1])
	right_column=pygame.Rect(res[0]/40+res[0]/2, 0, (res[0]/2)-((res[0]/40)*2), res[1])
	title_font=pygame.font.SysFont("arial", int(res[0]/30))
	txt_join=title_font.render("Dołącz do serwera", True, (0,0,0))
	txt_join_rect=txt_join.get_rect()
	txt_join_size=txt_join_rect.width
	txt_create=title_font.render("Stwórz serwer", True, (0,0,0))
	txt_create_rect=txt_create.get_rect()
	txt_create_size=txt_create_rect.width
	button_size=res[0]/35
	join_button=button(((res[0]/4)-(len("Dołącz")*((res[1]/10)/7)), (res[1]/10)*6), [button_size, button_size], (189,189,189), text="Dołącz")
	create_button=button(((res[0]/4)*3-(len("Stwórz")*((res[1]/10)/7)), (res[1]/10)*6), [button_size, button_size], (189,189,189), text="Stwórz")
	buttons=[join_button, create_button]
	playing=1
	
	while playing:
		win.fill((90,200,210))
		pygame.draw.rect(win,(90,180,180), left_column)
		pygame.draw.rect(win,(90,180,180), right_column)
		win.blit(txt_join, (res[0]/4-txt_join_size/2, (res[1]/10)*2))
		win.blit(txt_create, ((res[0]/4)*3-txt_create_size/2, (res[1]/10)*2))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				playing=0
				break
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				for box in boxes:
					if box.rect.collidepoint(event.pos):
						box.status=1
					else:
						box.status=0
			elif event.type == pygame.KEYDOWN:
				print(event.key)
				for box in boxes:
					if box.status==1:
						if event.key==8 and box.text!=0:
							box.text=box.text[:-1]
						elif len(box.text)<box.limit:
							box.text+=chr(event.key)
		for box in boxes:
			box.draw(win)
		for b in buttons:
			b.draw(win)
		pygame.display.update()
	