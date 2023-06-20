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
	global game_window, res
	kings_chess(game_window, res)
	
def play_online():
	global game_window, res
	online_menu(game_window, res, nick_input.get_value())
	
def options():
	global game_window, res, timers, max_time 
	opting=1
	font_size = int(win.get_size()[0]/45)
	left_column=pygame.Rect(res[0]/40, 0, (res[0]/2)-((res[0]/40)*2), res[1])
	right_column=pygame.Rect(res[0]/40+res[0]/2, 0, (res[0]/2)-((res[0]/40)*2), res[1])
	txt_timers=title_font.render("Zegary", True, (0,0,0))
	txt_timers_rect=txt_join.get_rect()
	txt_timers_size=txt_join_rect.width
	txt_res=title_font.render("Rozdzielczość", True, (0,0,0))
	txt_res_rect=txt_create.get_rect()
	txt_res_size=txt_create_rect.width
	while opting:
		win.fill((90,200,210))
		pygame.draw.rect(game_window,(90,180,180), left_column)
		pygame.draw.rect(game_window,(90,180,180), right_column)
		


pygame.init()
res=(800,600)
game_window = pygame.display.set_mode(res)
pygame.display.set_caption("Szachy Królewskie")

mainmenu = pygame_menu.Menu('Szachy królewskie', res[0], res[1], theme=themes.THEME_BLUE)
nick_input=mainmenu.add.text_input('Nick: ', default='Nick', maxchar=20)
mainmenu.add.button('Gra na jednym komputerze', play_local)
mainmenu.add.button('Gra sieciowa', play_online)
mainmenu.add.button("Opcje", options)
mainmenu.add.button('Wyjście', pygame_menu.events.EXIT)
 
#level = pygame_menu.Menu('Select a Difficulty', 600, 400, theme=themes.THEME_BLUE)
#level.add.selector('Difficulty:',[('Hard',1),('Easy',2)], onchange=set_difficulty)

mainmenu.mainloop(game_window)