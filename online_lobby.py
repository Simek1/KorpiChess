import pygame
import pygame_menu
import socket
from kings_chess import *
from requests import get


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
		win.blit(txt, (self.pos[0], self.pos[1]))
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
					self.text+=chr(letter)
		except Exception as e:
				print(e)
		
class chat_box(object):
	def __init__(self, pos, size, font_size):
		self.size=size
		self.pos=pos
		self.font_size=font_size
		self.font=pygame.font.SysFont("arial", self.font_size)
		test_text="test"
		test_text=self.font.render(test_text, True, (255,255,255))
		test_text_height=test_text.get_rect().height
		new_size=0
		while True:
			if new_size+test_text_height+3<=self.size[1]:
				new_size+=test_text_height+3
			else:
				self.size=(self.size[0],new_size)
				break
		self.size=(self.size[0], new_size)
		self.rect=pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
		self.chat_input=input_box((self.size[0],test_text_height), (self.pos[0], self.pos[1]+self.size[1]), self.font_size, 70, color=(128,128,128)) #zmienic aby tekst sie przesuwal w trakcie pisania
		self.not_converted=[]
		self.converted_msgs=[]
		self.max_msgs=self.size[1]//(test_text_height+3)
		self.y_pos=[x for x in range(int(self.pos[1]), int(self.pos[1]+self.size[1]+1), int(test_text_height+3))]
		print(self.y_pos)
	def update_chat(self, msgs):
		for x in msgs:
			if "<SERVER>" in x or "\chat" in x:
				if "\chat" in x:
					splited=x.split()
					msg=""
					for word in splited:
						if word!="\chat":
							msg+=word+" "
					msg=msg[:-1]
					self.not_converted.append(msg)
				else:
					self.not_converted.append(x)
	def draw(self, win):
		pygame.draw.rect(win, (100,100,100), self.rect)
		self.chat_input.draw(win)
		if self.not_converted!=[]:
			conv=[]
			for ms in self.not_converted:
				ren_ms=self.font.render(ms, True, (255,255,255))
				ren_ms_width=ren_ms.get_rect().width
				if ren_ms_width>self.size[0]:
					too_long=True
					splited_ms=ms.split()
					print(splited_ms, "splited")
					while too_long:
						for i in range(1,len(splited_ms)):
							ren_ms=self.font.render(" ".join(splited_ms[:-i]), True, (255,255,255))
							ren_ms_width=ren_ms.get_rect().width
							#print(" ".join(splited_ms)[:-i], i, len(splited_ms))
							if ren_ms_width<=self.size[0]:
								conv.append(ren_ms)
								splited_ms=splited_ms[-i:]
								#print(splited_ms, "ponowny split")
								ren_ms=self.font.render(" ".join(splited_ms), True, (255,255,255))
								ren_ms_width=ren_ms.get_rect().width
								if ren_ms_width<=self.size[0]:
									conv.append(ren_ms)
									too_long=False
								break
							elif i==len(splited_ms)-1:
								ren_ms=self.font.render(splited_ms[0], True, (255,255,255))
								conv.append(ren_ms)
								splited_ms=splited_ms[-1:]
								if splited_ms==[]:
									too_long=False
								break
				else:
					conv.append(ren_ms)
			self.not_converted=[]
			if len(self.converted_msgs)+len(conv)>self.max_msgs:
				diff=len(self.converted_msgs)+len(conv)-self.max_msgs
				self.converted_msgs=self.converted_msgs[diff:]
			for x in conv:
				self.converted_msgs.append(x)
		i=0
		for ms in self.converted_msgs:
			win.blit(ms, (self.pos[0], self.y_pos[i]))
			i+=1
			
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
		
		
def online_menu(win, res, nick):
	font_size = int(win.get_size()[0]/45)
	longest_ip="123.123.123.123"
	font = pygame.font.SysFont("arial", font_size)
	eg_render=font.render(longest_ip, True, (0, 0, 0))
	eg_render=eg_render.get_rect()
	ip_box_size=(eg_render.width, eg_render.height)
	try:
		externalip= get('https://api.ipify.org').content.decode('utf8')
	except:
		externalip="NaN"
	localip=socket.gethostbyname(socket.gethostname())
	ex_ip_txt=font.render("IP zewnętrzne: "+externalip, True, (0,0,0))
	local_ip_txt=font.render("Lokalne IP: "+str(localip), True, (0,0,0))
	ex_ip_pos=((res[0]/4)*3-ex_ip_txt.get_rect().width/2, res[1]/10*7)
	local_ip_pos=((res[0]/4)*3-local_ip_txt.get_rect().width/2, res[1]/10*8)
	join_ip_box=input_box(ip_box_size, ((res[0]/4)-(ip_box_size[0]/2),(res[1]/10)*3), font_size, 15,"", "IP serwera")
	join_port_box=input_box(ip_box_size, ((res[0]/4)-(ip_box_size[0]/2),(res[1]/10)*4), font_size, 8,"", "Port serwera")
	create_ip_box=input_box(ip_box_size, ((res[0]/4)*3-(ip_box_size[0]/2),(res[1]/10)*3), font_size, 15,"0.0.0.0", "IP serwera")
	create_port_box=input_box(ip_box_size, ((res[0]/4)*3-(ip_box_size[0]/2),(res[1]/10)*4), font_size, 8,"", "Port serwera")
	nick_box=input_box(ip_box_size, ((res[0]/4)*2-ip_box_size[0]/2, res[1]/10), font_size, 15, nick, "Nick: ")
	boxes=[join_ip_box, join_port_box, create_ip_box, create_port_box, nick_box]
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
	numpad_keys=[1073741922, 1073741913, 1073741914, 1073741915, 1073741916, 1073741917, 1073741918, 1073741919, 1073741920, 1073741921]
	menuing=1
	hosting=0
	connected=0
	
	while menuing:
		win.fill((90,200,210))
		pygame.draw.rect(win,(90,180,180), left_column)
		pygame.draw.rect(win,(90,180,180), right_column)
		win.blit(txt_join, (res[0]/4-txt_join_size/2, (res[1]/10)*2))
		win.blit(txt_create, ((res[0]/4)*3-txt_create_size/2, (res[1]/10)*2))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				menuing=0
				break
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				for box in boxes:
					if box.rect.collidepoint(event.pos):
						box.status=1
					else:
						box.status=0
				if join_button.rect.collidepoint(event.pos):
					try:
						connected=1
						menuing=0
						connect_to_server(int(join_port_box.text), join_ip_box.text, nick_box.text)
						chat=chat_box((res[1]-100, res[1]/5*3), (res[0]-res[1]+100, res[1]/5*2), font_size)
						new_msg=[]
						downloadThread=threading.Thread(target=download_msg, args=(new_msg,))
						downloadThread.start()
						waiting_txt=title_font.render("Oczekiwanie na rozpoczęcie przez hosta", True, (0,0,0))
						waiting_txt_rect=waiting_txt.get_rect()
						waiting_txt_pos=(res[0]/2-waiting_txt_rect.width/2, res[1]/2-waiting_txt_rect.height)
					except Exception as e:
						connected=0
						menuing=1
						print(e)
				if create_button.rect.collidepoint(event.pos):
					try:
						old_nicks={}
						start_server(create_port_box.text, create_ip_box.text)
						hosting=1
						menuing=0
						connect_to_server(create_port_box.text, localip, nick_box.text)
						txt_players=title_font.render("Gracze:", True, (0,0,0))
						txt_players_width=txt_players.get_rect().width/2
						chat=chat_box((res[1]-res[1]/6, res[1]/5*3), (res[0]-res[1]+res[1]/6, res[1]/5*2), font_size)
						new_msg=[]
						downloadThread=threading.Thread(target=download_msg, args=(new_msg,))
						downloadThread.start()
						start_button=inactive_button((res[0]/4-(res[0]/10)/2, res[1]/10*8), [res[0]/10, res[1]/10], (185, 182, 183), "Zacznij")
					except Exception as e:
						hosting=0
						menuing=1
						print(e)
			elif event.type == pygame.KEYDOWN:
				print(event.key)
				for box in boxes:
					if box.status==1:
						box.write(event.key, numpad_keys)
						break
		for box in boxes:
			box.draw(win)
		for b in buttons:
			b.draw(win)
		win.blit(ex_ip_txt, ex_ip_pos)
		win.blit(local_ip_txt, local_ip_pos)
		pygame.display.update()
	while hosting==1: #wersja lobby dla hosta
		if nicks!=old_nicks:
			txt_nicks=[]
			old_nicks=nicks.copy()
			i=3
			print(nicks, "nicks")
			for x in nicks:
				nic=font.render(nicks[x], True, (0,0,0))
				nic_width=nic.get_rect().width
				nic_pos=(res[0]/4-nic_width/2, res[1]/10*i)
				txt_nicks.append((nic, nic_pos))
				i-=1
				print(txt_nicks)
		if new_msg!=[]:
			chat.update_chat(new_msg)
			new_msg.clear()
			print(nicks)
		if len(nicks)<2:
			start_button.status=0
		else:
			start_button.status=1
		win.fill((185, 182, 183))
		pygame.draw.rect(win,(90,180,180), left_column)
		win.blit(txt_players, (res[0]/4-txt_players_width, 10))
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				hosting=0
				close_server()
				break
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if chat.chat_input.rect.collidepoint(event.pos):
					chat.chat_input.status=1
				else:
					chat.chat_input.status=0
				if start_button.rect.collidepoint(event.pos):
					if start_button.status==1:
						print("Start")
					else:
						send("\chat Potrzeba 2 graczy aby wystartować")
			elif event.type == pygame.KEYDOWN:
				if chat.chat_input.status==1:
					if event.key==13:
						if len(chat.chat_input.text)>0:
							send("\chat "+chat.chat_input.text)
							chat.chat_input.text=""
					else:
						chat.chat_input.write(event.key, numpad_keys)
		for x in txt_nicks:
			win.blit(x[0],x[1])
		chat.draw(win)
		start_button.draw(win)
		pygame.display.update()
	while connected==1: #Wersja lobby dla dołączającego gracza
		win.fill((90,200,210))
		win.blit(waiting_txt, waiting_txt_pos)
		if new_msg!=[]:
			chat.update_chat(new_msg)
			for x in new_msg:
				if x=="<SERVER>: Server został wyłączony.":
					connected=0
			new_msg.clear()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				connected=0
				send("!@#disc#@!")
				break
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if chat.chat_input.rect.collidepoint(event.pos):
					chat.chat_input.status=1
				else:
					chat.chat_input.status=0
			elif event.type == pygame.KEYDOWN:
				if chat.chat_input.status==1:
					if event.key==13:
						if len(chat.chat_input.text)>0:
							send("\chat "+chat.chat_input.text)
							chat.chat_input.text=""
					else:
						chat.chat_input.write(event.key, numpad_keys)
		chat.draw(win)
		pygame.display.update()

	