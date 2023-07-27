import pygame
import pygame_menu
from pygame_menu import themes
from kings_chess import *
from online_lobby import *
from kings_chess_online import *

class inactive_button(object):
	def __init__(self, pos, size, color, text=""):
		self.pos = pos
		self.size = size
		self.color = color
		self.text = text
		self.font_size = int(self.size[0]/4)
		self.undertext_font=pygame.font.SysFont("arial", int(self.font_size/4))
		self.font = pygame.font.SysFont("arial", self.font_size)
		self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
		self.status=0
	def draw(self, win):
		txt = self.font.render(self.text, True, (0, 0, 0))
		txt_rect=txt.get_rect()
		if self.status==0:
			pygame.draw.rect(win, self.color, self.rect)
		else:
			pygame.draw.rect(win, (self.color[0]+20, self.color[1]+20, self.color[2]+20), self.rect)
		win.blit(txt, (int(self.pos[0]+self.size[0]/2-txt_rect.width/2), int(self.pos[1]+self.size[1]/2-txt_rect.height/2)))


class input_box(object):
	def __init__(self, size, pos, font_size, limit, text="", uppertext="", color=""):
		self.size=size
		self.pos=pos
		self.font_size=font_size
		self.text=text
		self.limit=limit
		self.font = pygame.font.SysFont("arial", self.font_size)
		self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
		self.uppertext=uppertext
		self.status=0
		self.upper=0
		self.special=0
		self.sh_alph={"q":"Q","w":"W","e":"E","r":"R","t":"T","y":"Y","u":"U","i":"I","o":"O","p":"P","[":"{","]":"}","\\":"|",
			 "`":"~","1":"!","2":"@","3":"#","4":"$","5":"%","6":"^","7":"&","8":"*","9":"(","0":")","-":"_","=":"+",
			 "a":"A","s":"S","d":"D","f":"F","g":"G","h":"H","j":"J","k":"K","l":"L",";":":","'":"\"",
			 "z":"Z","x":"X","c":"C","v":"V","b":"B","n":"N","m":"M",",":"<",".":">","/":"?", 
			 "ą":"Ą", "ę":"Ę", "ł":"Ł", "ó":"Ó","ż":"Ż","ź":"Ź","ć":"Ć","ń":"Ń","ś":"Ś"}
		self.alt_alph={"a":"ą", "e":"ę", "l":"ł", "o":"ó","z":"ż","x":"ź", "c":"ć", "n":"ń", "s":"ś"}
		if color=="":
			self.color=(189,189,189)
		else:
			self.color=color
	def draw(self, win):
		txt = self.font.render(self.text, True, (0, 0, 0))
		if self.status==0:
			color=self.color
		else:
			color=(self.color[0]+30,self.color[1]+30,self.color[2]+30)
		pygame.draw.rect(win, color, self.rect)
		temp_txt=txt
		i=1
		while temp_txt.get_rect().width>self.size[0]:
			temp_txt=self.font.render(self.text[i:], True, (0, 0, 0))
			i+=1
		win.blit(temp_txt, (self.pos[0], self.pos[1]))
		if self.uppertext!="":
			txt=self.font.render(self.uppertext, True, (0, 0, 0))
			width=txt.get_rect().width
			win.blit(txt, (self.pos[0]-5-width, self.pos[1]))
	def write(self, letter, numpad_keys):
		try:
			if letter==8 and len(self.text)>0:
				self.text=self.text[:-1]
			elif len(self.text)<self.limit:
				if letter in numpad_keys:
					self.text+=str(numpad_keys.index(letter))
				else:
					letter=chr(letter)
					if self.special==1:
						if letter in self.alt_alph:
							letter=self.alt_alph[letter]
					if self.upper==1:
						if letter in self.sh_alph:
							letter=self.sh_alph[letter]
					self.text+=letter
		except Exception as e:
				print(e)

def play_local():
	global game_window, res, timers, max_time
	kings_chess(game_window, res, timers, max_time)
	
def play_online():
	global game_window, res, timers, max_time
	online_menu(game_window, res, nick_input.get_value(), timers, max_time)
	
def options():
	global game_window, res, timers, max_time, mainmenu, fscreen, nick_input, reint
	opting=1
	font_size = int(res[0]/45)
	deafult_font=pygame.font.SysFont("arial", font_size)
	title_font=pygame.font.SysFont("arial", int(res[0]/30))
	left_column=pygame.Rect(res[0]/40, 0, (res[0]/2)-((res[0]/40)*2), res[1])
	right_column=pygame.Rect(res[0]/40+res[0]/2, 0, (res[0]/2)-((res[0]/40)*2), res[1])
	txt_timers=title_font.render("Zegary", True, (0,0,0))
	txt_timers_rect=txt_timers.get_rect()
	txt_timers_size=txt_timers_rect.width
	txt_res=title_font.render("Rozdzielczość", True, (0,0,0))
	txt_res_rect=txt_res.get_rect()
	txt_res_size=txt_res_rect.width
	timers_switch_txt=deafult_font.render("Włącz/wyłącz zegar:", True, (0,0,0))
	timers_switch=inactive_button(((res[0]/4)/3+timers_switch_txt.get_rect().width, (res[1]/10)*4), [res[0]/12, res[1]/12], (185, 182, 183), "Włącz")
	def_res=inactive_button((res[0]/4*3 -res[0]/11/2, res[1]/10*4), [res[0]/11, res[1]/12], (185, 182, 183), "800x600")
	hd_res=inactive_button((res[0]/4*3 -res[0]/11/2, res[1]/10*5), [res[0]/11, res[1]/12], (185, 182, 183), "1280x720")
	fullhd_res=inactive_button((res[0]/4*3 -res[0]/11/2, res[1]/10*6), [res[0]/11, res[1]/12], (185, 182, 183), "1920x1080")
	fullscreen=inactive_button((res[0]/4*3 -res[0]/11/2, res[1]/10*7), [res[0]/11, res[1]/12], (185, 182, 183), "Pełny ekran")
	if fscreen==1:
		fullscreen.status=1
	else:
		fullscreen.status=0
	if res==(800,600):
		def_res.status=1
		hd_res.status=0
		fullhd_res.status=0
	elif res==(1280,720):
		def_res.status=0
		hd_res.status=1
		fullhd_res.status=0
	else:
		def_res.status=0
		hd_res.status=0
		fullhd_res.status=1
	res_buttons=[def_res, hd_res, fullhd_res, fullscreen]
	if timers==1:
		timers_switch.status=1
		timers_switch.text="Wyłącz"
	max_time_input=input_box([res[0]/20,timers_switch_txt.get_rect().height], ((res[0]/4)/3+timers_switch_txt.get_rect().width, (res[1]/10)*6), font_size, 3, uppertext="Czas gry(minuty)")
	max_time_input.text=str(int(max_time/60))
	numpad_keys=[1073741922, 1073741913, 1073741914, 1073741915, 1073741916, 1073741917, 1073741918, 1073741919, 1073741920, 1073741921]
	while opting:
		game_window.fill((90,200,210))
		pygame.draw.rect(game_window,(90,180,180), left_column)
		pygame.draw.rect(game_window,(90,180,180), right_column)
		game_window.blit(txt_timers, (res[0]/4-txt_timers_size/2, (res[1]/10)*2))
		game_window.blit(txt_res, ((res[0]/4)*3-txt_res_size/2, (res[1]/10)*2))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				opting=0
				with open("settings.txt", "w") as file:
					if max_time_input.text=="":
						max_time_input.text=1
					file.write(f"{str(timers_switch.status)}\n{str(int(max_time_input.text)*60)}\n{res}\n{fscreen}")
				timers=timers_switch.status
				max_time=int(max_time_input.text)*60
				print(max_time)
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if max_time_input.rect.collidepoint(event.pos):
					max_time_input.status=1
				else:
					max_time_input.status=0
				if timers_switch.rect.collidepoint(event.pos):
					if timers_switch.status==0:
						timers_switch.status=1
						timers_switch.text="Wyłącz"
					else:
						timers_switch.status=0
						timers_switch.text="Włącz"
				if def_res.rect.collidepoint(event.pos) and def_res.status==0:
					res=(800,600)
					if fscreen==0:
						pygame.display.set_mode(res)
					else:
						pygame.display.set_mode(res, pygame.FULLSCREEN)
					reint=1
					opting=0
				elif hd_res.rect.collidepoint(event.pos) and hd_res.status==0:
					res=(1280,720)
					if fscreen==0:
						pygame.display.set_mode(res)
					else:
						pygame.display.set_mode(res, pygame.FULLSCREEN)
					reint=1
					opting=0
				elif fullhd_res.rect.collidepoint(event.pos) and fullhd_res.status==0:
					res=(1920,1080)
					if fscreen==0:
						pygame.display.set_mode(res)
					else:
						pygame.display.set_mode(res, pygame.FULLSCREEN)
					reint=1
					opting=0
				if fullscreen.rect.collidepoint(event.pos):
					if fullscreen.status==1:
						pygame.display.set_mode(res)
						fullscreen.status=0
						fscreen=0
					else:
						pygame.display.set_mode(res, pygame.FULLSCREEN)
						fullscreen.status=1
						fscreen=1
			if event.type == pygame.KEYDOWN:
				if max_time_input.status==1:
					if event.key in (8, 49, 50, 51, 52, 53, 54, 55, 56, 57, 48, 1073741913 ,1073741914 ,1073741915, 1073741916, 1073741917, 1073741918 ,1073741919, 1073741920, 1073741921):
						max_time_input.write(event.key, numpad_keys)
				if event.key==27:
					opting=0
					with open("settings.txt", "w") as file:
						if max_time_input.text=="":
							max_time_input.text=1
						file.write(f"{str(timers_switch.status)}\n{str(int(max_time_input.text)*60)}\n{res}\n{fscreen}")
					timers=timers_switch.status
					max_time=int(max_time_input.text)*60
					print(max_time)
		game_window.blit(timers_switch_txt, ((res[0]/4)/3, (res[1]/10*4)+timers_switch.size[1]/2-timers_switch_txt.get_rect().height/2))
		for x in res_buttons:
			x.draw(game_window)
		
		timers_switch.draw(game_window)
		max_time_input.draw(game_window)
		pygame.display.update()

		
try:
	sett=open("settings.txt", "r")
	settings=sett.readlines()
	timers=int(settings[0])
	max_time=int(settings[1])
	res=eval(settings[2])
	fscreen=int(settings[3])
	sett.close()
except Exception as e:
	timers=0
	max_time=1800
	res=(800,600)
	fscreen=0
	print(e)
	

pygame.init()
game_window = pygame.display.set_mode(res)
if fscreen:
	pygame.display.set_mode(res, pygame.FULLSCREEN)
pygame.display.set_caption("Korpalski Chess")

mainmenu = pygame_menu.Menu('Korpalski Chess', res[0], res[1], theme=themes.THEME_BLUE)
nick_input=mainmenu.add.text_input('Nick: ', default='Nick', maxchar=20)
mainmenu.add.button('Gra na jednym komputerze', play_local)
mainmenu.add.button('Gra sieciowa', play_online)
mainmenu.add.button("Opcje", options)
mainmenu.add.button('Wyjście', pygame_menu.events.EXIT)

#level = pygame_menu.Menu('Select a Difficulty', 600, 400, theme=themes.THEME_BLUE)
#level.add.selector('Difficulty:',[('Hard',1),('Easy',2)], onchange=set_difficulty)

#mainmenu.mainloop(game_window)
running=1
reint=0
while running:
	pygame.time.Clock().tick(30)
	events = pygame.event.get()
	for event in events:
		if event.type == pygame.QUIT:
			running=0
		if event.type == pygame.KEYDOWN:
			if event.key==27:
				running=0
	if reint==1:
		reint=0
		mainmenu = pygame_menu.Menu('Korpalski Chess', res[0], res[1], theme=themes.THEME_BLUE)
		nick_input=mainmenu.add.text_input('Nick: ', default='Nick', maxchar=20)
		mainmenu.add.button('Gra na jednym komputerze', play_local)
		mainmenu.add.button('Gra sieciowa', play_online)
		mainmenu.add.button("Opcje", options)
		mainmenu.add.button('Wyjście', pygame_menu.events.EXIT)
		options()
	if mainmenu.is_enabled():
		mainmenu.update(events)
		mainmenu.draw(game_window)
	
	pygame.display.update()
	
pygame.quit()

