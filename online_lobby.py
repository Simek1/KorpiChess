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
			if "<SERVER>" in x or "@chat" in x:
				if "@chat" in x:
					splited=x.split()
					msg=""
					for word in splited:
						if word!="@chat":
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

class color_rects(object):
	def __init__(self, pos, size, status):
		self.pos=pos
		self.size=size
		self.status=status
		self.rect=pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
		self.frame=pygame.Rect(self.pos[0]-2, self.pos[1]-2, self.size[0]+4, self.size[1]+4)
	def draw(self, win):
		if self.status==1:
			color=(0,0,0)
			fr_color=(255,255,255)
		else:
			color=(255,255,255)
			fr_color=(0,0,0)
		pygame.draw.rect(win, fr_color, self.frame)
		pygame.draw.rect(win, color, self.rect)		

def kings_chess_online(game_window, res, player_name, player_color, msgs, chat_history):
	res_b = (res[1]-res[1]/6, res[1]-res[1]/6)
	bg_color = (185, 182, 183)
	
	font_size = int(game_window.get_size()[0]/45)
	font = font = pygame.font.SysFont("arial", font_size)
	
	board_png = pygame.image.load('images/board.png')
	board_png = pygame.transform.scale(board_png, res_b)

	pawn_b_png = pygame.image.load('images/pawn_b.png')
	pawn_w_png = pygame.image.load('images/pawn_w.png')
	king_b_png = pygame.image.load('images/king_b.png')
	king_w_png = pygame.image.load('images/king_w.png')
	queen_b_png = pygame.image.load('images/queen_b.png')
	queen_w_png = pygame.image.load('images/queen_w.png')
	bishop_b_png = pygame.image.load('images/bishop_b.png')
	bishop_w_png = pygame.image.load('images/bishop_w.png')
	knight_b_png = pygame.image.load('images/knight_b.png')
	knight_w_png = pygame.image.load('images/knight_w.png')
	rook_b_png = pygame.image.load('images/rook_b.png')
	rook_w_png = pygame.image.load('images/rook_w.png')

	pawn_res = int(res_b[0]/8)
	pawn_res = (pawn_res, pawn_res)

	pawn_b_png = pygame.transform.scale(pawn_b_png, pawn_res)
	pawn_w_png = pygame.transform.scale(pawn_w_png, pawn_res)
	king_b_png = pygame.transform.scale(king_b_png, pawn_res)
	king_w_png = pygame.transform.scale(king_w_png, pawn_res)
	queen_b_png = pygame.transform.scale(queen_b_png, pawn_res)
	queen_w_png = pygame.transform.scale(queen_w_png, pawn_res)
	bishop_b_png = pygame.transform.scale(bishop_b_png, pawn_res)
	bishop_w_png = pygame.transform.scale(bishop_w_png, pawn_res)
	knight_b_png = pygame.transform.scale(knight_b_png, pawn_res)
	knight_w_png = pygame.transform.scale(knight_w_png, pawn_res)
	rook_b_png = pygame.transform.scale(rook_b_png, pawn_res)
	rook_w_png = pygame.transform.scale(rook_w_png, pawn_res)

	board=ch_board(board_png,(0,0), res_b)
	
	again_button = button((res[0]/4-res[0]/20, res[1]/4-res[1]/20), [res[0]/10, res[1]/10], (139, 139, 139), "Zagraj ponownie")
	quit_button = button(((res[0]/4-res[0]/20)*3, res[1]/4-res[1]/20), [res[0]/10, res[1]/10], (139, 139, 139), "Wyjdź z gry")
	
	end_game_w = notification([20, 20], [res[0]-40, res[1]/2-20], (100, 215, 220), "Koniec gry", font_size*2)
	
	# tworzenie okna zmiany pionka
	transform_w = notification([20, 20], [res[0]-40, res[1]/2-20], (185, 182, 183), "Wybierz figurę w którą zamienić pionka", font_size*2)
	
	rook_b_button = button([transform_w.pos[0]+transform_w.size[0]/5-pawn_res[0]/2, transform_w.pos[1]+transform_w.size[1]/2-pawn_res[1]/2], pawn_res, (0, 0, 0), undertext="Wieża", graph=rook_b_png)
	knight_b_button = button([(transform_w.pos[0]+transform_w.size[0]/5-pawn_res[0]/2)*2, transform_w.pos[1]+transform_w.size[1]/2-pawn_res[1]/2], pawn_res, (0, 0, 0), undertext="Koń", graph=knight_b_png)
	bishop_b_button = button([(transform_w.pos[0]+transform_w.size[0]/5-pawn_res[0]/2)*3, transform_w.pos[1]+transform_w.size[1]/2-pawn_res[1]/2], pawn_res, (0, 0, 0), undertext="Goniec", graph=bishop_b_png)
	queen_b_button = button([(transform_w.pos[0]+transform_w.size[0]/5-pawn_res[0]/2)*4, transform_w.pos[1]+transform_w.size[1]/2-pawn_res[1]/2], pawn_res, (0, 0, 0), undertext="Królowa", graph=queen_b_png)
	
	rook_w_button = button([transform_w.pos[0]+transform_w.size[0]/5-pawn_res[0]/2,transform_w.pos[1]+transform_w.size[1]/2-pawn_res[1]/2], pawn_res, (0, 0, 0), undertext="Wieża", graph=rook_w_png)
	knight_w_button = button([(transform_w.pos[0]+transform_w.size[0]/5-pawn_res[0]/2)*2, transform_w.pos[1]+transform_w.size[1]/2-pawn_res[1]/2], pawn_res, (0, 0, 0), undertext="Koń", graph=knight_w_png)
	bishop_w_button = button([(transform_w.pos[0]+transform_w.size[0]/5-pawn_res[0]/2)*3, transform_w.pos[1]+transform_w.size[1]/2-pawn_res[1]/2], pawn_res, (0, 0, 0), undertext="Goniec", graph=bishop_w_png)
	queen_w_button = button([(transform_w.pos[0]+transform_w.size[0]/5-pawn_res[0]/2)*4, transform_w.pos[1]+transform_w.size[1]/2-pawn_res[1]/2], pawn_res, (0, 0, 0), undertext="Królowa", graph=queen_w_png)
	
	#######
	
	# Tworzenie okna dodawania pionka
	
	add_w = notification([20, 20], [res[0]-40, res[1]/2-20],(185, 182, 183), "Wybierz figurę", font_size*2)
	
	
	
	add_rook_b = button([add_w.pos[0]+add_w.size[0]/6-pawn_res[0]/2, add_w.pos[1]+add_w.size[1]/2-pawn_res[1]/2], pawn_res, (0, 0, 0), undertext="Wieża(2)", graph=rook_b_png)
	add_knight_b = button([(add_w.pos[0]+add_w.size[0]/6-pawn_res[0]/2)*2, add_w.pos[1]+add_w.size[1]/2-pawn_res[1]/2], pawn_res, (0, 0, 0), undertext="Koń(2)", graph=knight_b_png)
	add_bishop_b = button([(add_w.pos[0]+add_w.size[0]/6-pawn_res[0]/2)*3, add_w.pos[1]+add_w.size[1]/2-pawn_res[1]/2], pawn_res, (0, 0, 0), undertext="Goniec(2)", graph=bishop_b_png)
	add_queen_b = button([(add_w.pos[0]+add_w.size[0]/6-pawn_res[0]/2)*4, add_w.pos[1]+add_w.size[1]/2-pawn_res[1]/2], pawn_res, (0, 0, 0), undertext="Królowa(1)", graph=queen_b_png)
	add_pawn_b = button([(add_w.pos[0]+add_w.size[0]/6-pawn_res[0]/2)*5, add_w.pos[1]+add_w.size[1]/2-pawn_res[1]/2], pawn_res, (0, 0, 0), undertext="Pionek(8)", graph=pawn_b_png)
	add_king_b = button([(add_w.pos[0]+add_w.size[0]/2-pawn_res[0]/2), add_w.pos[1] + add_w.size[1]/2-pawn_res[1]/2], pawn_res, (0, 0, 0), undertext="Król", graph=king_b_png)
	
	
	
	
	
	add_rook_w = button([add_w.pos[0]+add_w.size[0]/6-pawn_res[0]/2, add_w.pos[1]+add_w.size[1]/2-pawn_res[1]/2], pawn_res, (0, 0, 0), undertext="Wieża(2)", graph=rook_w_png)
	add_knight_w = button([(add_w.pos[0]+add_w.size[0]/6-pawn_res[0]/2)*2, add_w.pos[1]+add_w.size[1]/2-pawn_res[1]/2], pawn_res, (0, 0, 0), undertext="Koń(2)", graph=knight_w_png)
	add_bishop_w = button([(add_w.pos[0]+add_w.size[0]/6-pawn_res[0]/2)*3, add_w.pos[1]+add_w.size[1]/2-pawn_res[1]/2], pawn_res, (0, 0, 0), undertext="Goniec(2)", graph=bishop_w_png)
	add_queen_w = button([(add_w.pos[0]+add_w.size[0]/6-pawn_res[0]/2)*4, add_w.pos[1]+add_w.size[1]/2-pawn_res[1]/2], pawn_res, (0, 0, 0), undertext="Królowa(1)", graph=queen_w_png)
	add_pawn_w = button([(add_w.pos[0]+add_w.size[0]/6-pawn_res[0]/2)*5, add_w.pos[1]+add_w.size[1]/2-pawn_res[1]/2], pawn_res, (0, 0, 0), undertext="Pionek(8)", graph=pawn_w_png)
	add_king_w = button([(add_w.pos[0]+add_w.size[0]/2-pawn_res[0]/2), add_w.pos[1] + add_w.size[1]/2-pawn_res[1]/2], pawn_res, (0, 0, 0), undertext="Król", graph=king_w_png)
	
	add_button = button([board.res[1]-(board.res[1]/6)*2, (board.res[1]/6)*6],  [20, 50], (205, 202, 203), text="Dodaj figurę")
	
	chat=chat_box((res[1]-res[1]/6, res[1]/5*3), (res[0]-res[1]+res[1]/6, res[1]/5*2), font_size)
	chat.converted_msgs=chat_history
	#te elementy muszą zostać zrestartowane w każdej grze
	board.pawns_matrix=[[0 for x in range(0, 8)] for x in range(0, 8)]
	black_pawns = []
	white_pawns = []
	count_b = {"pawn": 8,
			   "rook": 2,
			   "knight": 2,
			   "bishop": 2,
			   "queen": 1,
			   "king": 1}
	count_w = {"pawn": 8,
			   "rook": 2,
			   "knight": 2,
			   "bishop": 2,
			   "queen": 1,
			   "king": 1}
	white_watch = stopwatch("w", font)
	black_watch = stopwatch("b", font)
	w_destroyed={"pawn": 0,
			   "rook": 0,
			   "knight": 0,
			   "bishop": 0,
			   "queen": 0,
			   "king": 0}
	b_destroyed={"pawn": 0,
			   "rook": 0,
			   "knight": 0,
			   "bishop": 0,
			   "queen": 0,
			   "king": 0}

	transform= False
	check = False
	playing = True
	click = 0
	hold = 0
	turn = "white"
	turn_txt = "Tura białych"
	turn_pawns = white_pawns
	en = []
	check_txt = ""
	adding = False
	check_add=[]
	figure=0
	if player_color=="white":
		opponent_color="black"
	else:
		opponent_color="white"

	deciding = True
	first_frame = True
	black_watch.pause_timer()
	while playing:
		while transform: #Kiedy pionek zmieniany jest na inną figurę
			transform_w.draw(game_window)
			if tr.color=="w":
				rook_w_button.undertext="Wieża("+str(b_destroyed["rook"])+")"
				rook_w_button.draw(game_window)
				knight_w_button.undertext="Rycerz("+str(b_destroyed["knight"])+")"
				knight_w_button.draw(game_window)
				bishop_w_button.undertext="Goniec("+str(b_destroyed["bishop"])+")"
				bishop_w_button.draw(game_window)
				queen_w_button.undertext="Królowa("+str(b_destroyed["queen"])+")"
				queen_w_button.draw(game_window)
			else:
				rook_b_button.undertext="Wieża("+str(w_destroyed["rook"])+")"
				rook_b_button.draw(game_window)
				knight_b_button.undertext="Rycerz("+str(w_destroyed["knight"])+")"
				knight_b_button.draw(game_window)
				bishop_b_button.undertext="Goniec("+str(w_destroyed["bishop"])+")"
				bishop_b_button.draw(game_window)
				queen_b_button.undertext="Królowa("+str(w_destroyed["queen"])+")"
				queen_b_button.draw(game_window)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					playing=False
					deciding=False
					running=False
					transform==False
					pygame.quit()
				elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					if tr.color=="w":
						if rook_w_button.rect.collidepoint(event.pos) and b_destroyed["rook"]>0:
							b_destroyed["rook"]-=1
							tr.transform("rook", rook_w_png)
							transform=False
							send(f'@transform{t_type} {old_pos} {tr.pos} "rook"')
							send(f"@time {white_watch.remaining_time}")
						elif knight_w_button.rect.collidepoint(event.pos) and b_destroyed["knight"]>0:
							b_destroyed["knight"]-=1
							tr.transform("knight", knight_w_png)
							transform=False
							send(f'@transform{t_type} {old_pos} {tr.pos} "knight"')
							send(f"@time {white_watch.remaining_time}")
						elif bishop_w_button.rect.collidepoint(event.pos) and b_destroyed["bishop"]>0:
							b_destroyed["bishop"]-=1
							tr.transform("bishop", bishop_w_png)
							transform=False
							send(f'@transform{t_type} {old_pos} {tr.pos} "bishop"')
							send(f"@time {white_watch.remaining_time}")
						elif queen_w_button.rect.collidepoint(event.pos) and b_destroyed["queen"]>0:
							b_destroyed["queen"]-=1
							tr.transform("queen", queen_w_png)
							transform=False
							send(f'@transform{t_type} {old_pos} {tr.pos} "queen"')
							send(f"@time {white_watch.remaining_time}")
					else:
						if rook_b_button.rect.collidepoint(event.pos) and w_destroyed["rook"]>0:
							w_destroyed["rook"]-=1
							tr.transform("rook", rook_b_png)
							transform=False
							send(f'@transform{t_type} {old_pos} {tr.pos} "rook"')
							send(f"@time {black_watch.remaining_time}")  
						elif knight_b_button.rect.collidepoint(event.pos) and w_destroyed["knight"]>0:
							w_destroyed["knight"]-=1
							tr.transform("knight", knight_b_png)
							transform=False
							send(f'@transform{t_type} {old_pos} {tr.pos} "knight"')
							send(f"@time {black_watch.remaining_time}")  
						elif bishop_b_button.rect.collidepoint(event.pos) and w_destroyed["bishop"]>0:
							w_destroyed["bishop"]-=1
							tr.transform("bishop", bishop_b_png)
							transform=False
							send(f'@transform{t_type} {old_pos} {tr.pos} "bishop"')
							send(f"@time {black_watch.remaining_time}")  
						elif queen_b_button.rect.collidepoint(event.pos) and w_destroyed["queen"]>0:
							w_destroyed["queen"]-=1
							tr.transform("queen", queen_b_png)
							transform=False
							send('@transform{t_type} {old_pos} {tr.pos} "queen"')
							send(f"@time {black_watch.remaining_time}")  
			if transform==False:
				en=is_check(turn, white_pawns, black_pawns, board, game_window, w_destroyed, b_destroyed)
				if en!=[]: #blokowanie ruchow gdy jest szach
					#aktualizacja pozycji na pawn_matrix aby poprawnie sprwadzić możliwe ruchy przy szachu
					for white_pawn in white_pawns:
						white_pawn.draw(game_window, board)
					for black_pawn in black_pawns:
						black_pawn.draw(game_window, board)
					check_txt=is_mat(en, turn, white_pawns, black_pawns, board, game_window, w_destroyed, b_destroyed)
			pygame.display.update()
		while adding:  # Dodawanie figury na szachownice
			if figure==0:
				add_w.draw(game_window)
				if turn == "white":
					if count_w["king"]==0:
						add_rook_w.undertext="Wieża("+str(count_w["rook"])+")"
						add_rook_w.draw(game_window)
						add_knight_w.undertext="Rycerz("+str(count_w["knight"])+")"
						add_knight_w.draw(game_window)
						add_bishop_w.undertext="Goniec("+str(count_w["bishop"])+")"
						add_bishop_w.draw(game_window)
						add_queen_w.undertext="Królowa("+str(count_w["queen"])+")"
						add_queen_w.draw(game_window)
						add_pawn_w.undertext="Pionek("+str(count_w["pawn"])+")"
						add_pawn_w.draw(game_window)
					else:
						add_king_w.draw(game_window)
				else:
					if count_b["king"]==0:
						add_rook_b.undertext="Wieża("+str(count_b["rook"])+")"
						add_rook_b.draw(game_window)
						add_knight_b.undertext="Rycerz("+str(count_b["knight"])+")"
						add_knight_b.draw(game_window)
						add_bishop_b.undertext="Goniec("+str(count_b["bishop"])+")"
						add_bishop_b.draw(game_window)
						add_queen_b.undertext="Królowa("+str(count_b["queen"])+")"
						add_queen_b.draw(game_window)
						add_pawn_b.undertext="Pionek("+str(count_b["pawn"])+")"
						add_pawn_b.draw(game_window)
					else:
						add_king_b.draw(game_window)
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						playing = False
						deciding = False
						running = False
						adding == False
						pygame.quit()
					elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #Sprawdzenie która figura została wybrana
						temp=0
						if turn == "white":
							if count_w["king"]==0:
								if add_rook_w.rect.collidepoint(event.pos) and count_w["rook"]>0:
									figure="rook"
									temp=pawn(rook_w_png, (-1,-1), pawn_res, "rook", "w")
								elif add_knight_w.rect.collidepoint(event.pos) and count_w["knight"]>0:
									figure="knight"
									temp=pawn(knight_w_png, (-1,-1), pawn_res, "knight", "w")
								elif add_bishop_w.rect.collidepoint(event.pos) and count_w["bishop"]>0:
									figure="bishop"
									temp=pawn(bishop_w_png, (-1,-1), pawn_res, "bishop", "w")
								elif add_queen_w.rect.collidepoint(event.pos) and count_w["queen"]>0:
									figure="queen"
									temp=pawn(queen_w_png, (-1,-1), pawn_res, "queen", "w")
								elif add_pawn_w.rect.collidepoint(event.pos) and count_w["pawn"]>0:
									figure="pawn"
									temp=pawn(pawn_w_png, (-1,-1), pawn_res, "pawn", "w")
							else:
								if add_king_w.rect.collidepoint(event.pos):
									figure="king"
									temp=pawn(king_w_png, (-1,-1), pawn_res, "king", "w")
						else:
							if count_b["king"]==0:
								if add_rook_b.rect.collidepoint(event.pos) and count_b["rook"]>0:
									figure="rook"
									temp=pawn(rook_b_png, (-1,-1), pawn_res, "rook", "b")
								elif add_knight_b.rect.collidepoint(event.pos) and count_b["knight"]>0:
									figure="knight"
									temp=pawn(knight_b_png, (-1,-1), pawn_res, "knight", "b")
								elif add_bishop_b.rect.collidepoint(event.pos) and count_b["bishop"]>0:
									figure="bishop"
									temp=pawn(bishop_b_png, (-1,-1), pawn_res, "bishop", "b")
								elif add_queen_b.rect.collidepoint(event.pos) and count_b["queen"]>0:
									figure="queen"
									temp=pawn(queen_b_png, (-1,-1), pawn_res, "queen", "b")
								elif add_pawn_b.rect.collidepoint(event.pos) and count_b["pawn"]>0:
									figure="pawn"
									temp=pawn(pawn_b_png, (-1,-1), pawn_res, "pawn", "b")								
							else:
								if add_king_b.rect.collidepoint(event.pos):
									figure="king"
									temp=pawn(king_b_png, (-1,-1), pawn_res, "king", "b")
						if not add_w.rect.collidepoint(event.pos) and temp==0:
							adding=0
							check_add=[]

			else: #Postawienie wybranej figury na szachownicty
				possible_pos=board.add_positions(white_pawns, black_pawns, turn, temp, w_destroyed, b_destroyed, game_window)
				position_rects=[move_rect(x, board.area) for x in possible_pos]
				if check_txt!="":
					possible_pos=check_add
					position_rects=[move_rect(x, board.area) for x in possible_pos]
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						playing = False
						deciding = False
						running = False
						adding == False
						pygame.quit()
					if event.type == pygame.MOUSEBUTTONUP:
						mouse_pos = pygame.mouse.get_pos()
						x=-1
						y=-1
						i=0
						for area in board.pos_areas():
							if area[0] < mouse_pos[0] and area[1] > mouse_pos[0]:
								x = i
							if area[0] < mouse_pos[1] and area[1] > mouse_pos[1]:
								y = i
							i += 1
						if x!=-1 and y!=-1 and [x,y] in possible_pos:
							board.append_figure(temp, (x,y), white_pawns, black_pawns)
							send(f"@add {(x,y)} {temp.type}")
							if player_color=="white":
								send(f"@time {white_watch.remaining_time}")
							else:
								send(f"@time {black_watch.remaining_time}")  
							adding=0
							if temp.color=="w":
								count_w[temp.type]-=1
							else:
								count_b[temp.type]-=1
							en=[]
							check_add=[]
							if turn == "white":
								turn = "black"
								turn_pawns = black_pawns
								turn_txt = "Tura czarnych"
								black_watch.resume()
								white_watch.pause_timer()
							else:
								turn = "white"
								turn_pawns = white_pawns
								turn_txt = "Tura białych"
								white_watch.resume()
								black_watch.pause_timer()
							check_txt=""
						figure=0
						temp=0
					game_window.fill(bg_color)
					board.draw(game_window)
					for white_pawn in white_pawns:
						white_pawn.draw(game_window, board)
					for black_pawn in black_pawns:
						black_pawn.draw(game_window, board)
					white_watch.update(game_window, board)
					black_watch.update(game_window, board)
					for x in position_rects:
						x.draw_moves(game_window, board)
					if temp!=0:
						mouse_pos = pygame.mouse.get_pos()
						temp.mouse_dragging(game_window, mouse_pos)
					pygame.display.update()

				
			if adding == False:
				en = is_check(turn, white_pawns, black_pawns, board, game_window, w_destroyed, b_destroyed)
				if en != []:  # blokowanie ruchow gdy jest szach
					# aktualizacja pozycji na pawn_matrix aby poprawnie sprwadzić możliwe ruchy przy szachu
					for white_pawn in white_pawns:
						white_pawn.draw(game_window, board)
					for black_pawn in black_pawns:
						black_pawn.draw(game_window, board)
					check_txt=is_mat(en, turn, white_pawns, black_pawns, board, game_window, w_destroyed, b_destroyed)
			pygame.display.update()
		# if black_watch.remaining_time==0 or white_watch.remaining_time==0 or check_txt=="Szach-Mat!" or ("king" not in [p.type for p in white_pawns]) or ("king" not in [p.type for p in black_pawns]):
		if black_watch.remaining_time == 0 or white_watch.remaining_time == 0 or check_txt == "Szach-Mat!" or (w_destroyed["king"]==1 or b_destroyed["king"]==1):
			playing = False
		if msgs!=[]: #dorobic filtrowanie wiadomoscie ze wzgledu na \ i sprawdzic czy ta lista bedzie sie akutalizowac, jesli nie to sprobowac zrobic z niej zmienna globalna
			chat.update_chat(msgs)
			for x in msgs: #dorobic dzialania typu transformacja i sprawdzanie szacha uwzględnienie aby nie wykonywało się to dla osoby która wysłąła wiadomosc
				if "@chat" not in x and player_name not in x:
					if "@move" in x:
						x=x.split()
						apos=eval(x[2]+x[3])
						mve=eval(x[4]+x[5])
						if player_color=="white":
							for f in black_pawns:
								if f.pos==apos:
									f.pos=mve
									break
							turn = "white"
							turn_pawns = white_pawns
							turn_txt = "Tura białych"
							white_watch.resume()
							black_watch.pause_timer()							
						else:
							for f in white_pawns:
								if f.pos==apos:
									f.pos=mve
									break
							turn = "black"
							turn_pawns = black_pawns
							turn_txt = "Tura czarnych"
							black_watch.resume()
							white_watch.pause_timer()
						en = is_check(turn, white_pawns, black_pawns, board, game_window, w_destroyed, b_destroyed)
						if en != []:  # blokowanie ruchow gdy jest szach
							# aktualizacja pozycji na pawn_matrix aby poprawnie sprwadzić możliwe ruchy przy szachu
							for white_pawn in white_pawns:
								white_pawn.draw(game_window, board)
							for black_pawn in black_pawns:
								black_pawn.draw(game_window, board)
							check_txt=is_mat(en, turn, white_pawns, black_pawns, board, game_window, w_destroyed, b_destroyed)
						#endturn
					if "@attack" in x:
						x=x.split()
						apos=eval(x[2]+x[3])
						mve=eval(x[4]+x[5])
						print(mve, opponent_color, player_color)
						destroy_enemy(mve, opponent_color, white_pawns, black_pawns, w_destroyed, b_destroyed)
						if player_color=="white":
							for f in black_pawns:
								if f.pos==apos:
									f.pos=mve
									break
							turn = "white"
							turn_pawns = white_pawns
							turn_txt = "Tura białych"
							white_watch.resume()
							black_watch.pause_timer()
						else:
							for f in white_pawns:
								if f.pos==apos:
									f.pos=mve
									break
							turn = "black"
							turn_pawns = black_pawns
							turn_txt = "Tura czarnych"
							black_watch.resume()
							white_watch.pause_timer()
						en = is_check(turn, white_pawns, black_pawns, board, game_window, w_destroyed, b_destroyed)
						if en != []:  # blokowanie ruchow gdy jest szach
							# aktualizacja pozycji na pawn_matrix aby poprawnie sprwadzić możliwe ruchy przy szachu
							for white_pawn in white_pawns:
								white_pawn.draw(game_window, board)
							for black_pawn in black_pawns:
								black_pawn.draw(game_window, board)
							check_txt=is_mat(en, turn, white_pawns, black_pawns, board, game_window, w_destroyed, b_destroyed)
					if "@transformattack" in x:
						apos=eval(x[2]+x[3])
						mve=eval(x[4]+x[5])
						fig=x[6]
						destroy_enemy(mve, opponent_color, white_pawns, black_pawns, w_destroyed, b_destroyed)
						if player_color=="white":
							for f in black_pawns:
								if f.pos==apos:
									f.pos=mve
									break
							turn = "white"
							turn_pawns = white_pawns
							turn_txt = "Tura białych"
							white_watch.resume()
							black_watch.pause_timer()
						else:
							for f in white_pawns:
								if f.pos==apos:
									f.pos=mve
									break
							turn = "black"
							turn_pawns = black_pawns
							turn_txt = "Tura czarnych"
							black_watch.resume()
							white_watch.pause_timer()
						if player_color=="white":
							if fig=="queen":
								f.transform("queen", queen_b_png)
							if fig=="knight":
								f.transform("knight", knight_b_png)
							if fig=="rook":
								f.transform("rook", rook_b_png)
							if fig=="bishop":
								f.transform("bishop", bishop_b_png)
						else:
							if fig=="queen":
								f.transform("queen", queen_w_png)
							if fig=="knight":
								f.transform("knight", knight_w_png)
							if fig=="rook":
								f.transform("rook", rook_w_png)
							if fig=="bishop":
								f.transform("bishop", bishop_w_png)
						en=is_check(turn, white_pawns, black_pawns, board, game_window, w_destroyed, b_destroyed)
						if en!=[]: #blokowanie ruchow gdy jest szach
							#aktualizacja pozycji na pawn_matrix aby poprawnie sprwadzić możliwe ruchy przy szachu
							for white_pawn in white_pawns:
								white_pawn.draw(game_window, board)
							for black_pawn in black_pawns:
								black_pawn.draw(game_window, board)
							check_txt=is_mat(en, turn, white_pawns, black_pawns, board, game_window, w_destroyed, b_destroyed)
					if "@transformmove" in x:
						x=x.split()
						apos=eval(x[2]+x[3])
						mve=eval(x[4]+x[5])
						fig=x[6]
						if player_color=="white":
							for f in black_pawns:
								if f.pos==apos:
									f.pos=mve
									break
							turn = "white"
							turn_pawns = white_pawns
							turn_txt = "Tura białych"
							white_watch.resume()
							black_watch.pause_timer()
						else:
							for f in white_pawns:
								if f.pos==apos:
									f.pos=mve
									break
							turn = "black"
							turn_pawns = black_pawns
							turn_txt = "Tura czarnych"
							black_watch.resume()
							white_watch.pause_timer()
						if player_color=="white":
							if fig=="queen":
								f.transform("queen", queen_b_png)
							if fig=="knight":
								f.transform("knight", knight_b_png)
							if fig=="rook":
								f.transform("rook", rook_b_png)
							if fig=="bishop":
								f.transform("bishop", bishop_b_png)
						else:
							if fig=="queen":
								f.transform("queen", queen_w_png)
							if fig=="knight":
								f.transform("knight", knight_w_png)
							if fig=="rook":
								f.transform("rook", rook_w_png)
							if fig=="bishop":
								f.transform("bishop", bishop_w_png)
						en=is_check(turn, white_pawns, black_pawns, board, game_window, w_destroyed, b_destroyed)
						if en!=[]: #blokowanie ruchow gdy jest szach
							#aktualizacja pozycji na pawn_matrix aby poprawnie sprwadzić możliwe ruchy przy szachu
							for white_pawn in white_pawns:
								white_pawn.draw(game_window, board)
							for black_pawn in black_pawns:
								black_pawn.draw(game_window, board)
							check_txt=is_mat(en, turn, white_pawns, black_pawns, board, game_window, w_destroyed, b_destroyed)
					if "@add" in x:
						x=x.split()
						apos=eval(x[2]+x[3])
						fig=x[4]
						if player_color=="white":
							if fig=="pawn":
								afig=pawn(pawn_b_png, apos, pawn_res, "pawn", "b")
							if fig=="queen":
								afig=pawn(queen_b_png, apos, pawn_res, "queen", "b")
							if fig=="king":
								afig=pawn(king_b_png, apos, pawn_res, "king", "b")
							if fig=="bishop":
								afig=pawn(bishop_b_png, apos, pawn_res, "bishop", "b")
							if fig=="rook":
								afig=pawn(rook_b_png, apos, pawn_res, "rook", "b")
							if fig=="knight":
								afig=pawn(knight_b_png, apos, pawn_res, "knight", "b")
							turn = "white"
							turn_pawns = white_pawns
							turn_txt = "Tura białych"
							white_watch.resume()
							black_watch.pause_timer()
						else:
							if fig=="pawn":
								afig=pawn(pawn_w_png, apos, pawn_res, "pawn", "w")
							if fig=="queen":
								afig=pawn(queen_w_png, apos, pawn_res, "queen", "w")
							if fig=="king":
								afig=pawn(king_w_png, apos, pawn_res, "king", "w")
							if fig=="bishop":
								afig=pawn(bishop_w_png, apos, pawn_res, "bishop", "w")
							if fig=="rook":
								afig=pawn(rook_w_png, apos, pawn_res, "rook", "w")
							if fig=="knight":
								afig=pawn(knight_w_png, apos, pawn_res, "knight", "w")
							turn = "black"
							turn_pawns = black_pawns
							turn_txt = "Tura czarnych"
							black_watch.resume()
							white_watch.pause_timer()
						board.append_figure(afig, apos, white_pawns, black_pawns)
					if "@time" in x:
						rm_time=eval(x.split()[2])
						if player_color=="white":
							black_watch.remaining_time=rm_time
						else:
							white_watch_remaining_time=rm_time
			msgs.clear()
		pygame.time.Clock().tick(30)
		game_window.fill(bg_color)
		board.draw(game_window)
		add_button.draw(game_window)
		game_window.blit(font.render(turn_txt, True, (0, 0, 0)), (board.res[0]+15, 15))
		game_window.blit(font.render(check_txt, True, (0, 0, 0)), (board.res[0]+15, board.res[1]/2))
		white_watch.update(game_window, board)
		black_watch.update(game_window, board)

		for white_pawn in white_pawns:
			white_pawn.draw(game_window, board)
		for black_pawn in black_pawns:
			black_pawn.draw(game_window, board)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				playing = False
				deciding = False
				running = False
			# wybranie trzymanej figury
			if pygame.mouse.get_pressed()[0]  and turn==player_color:
				if click == 0:
					mouse_pos = list(pygame.mouse.get_pos())
					x = -1
					y = -1
					i = 0
					for area in board.pos_areas():
						if area[0] < mouse_pos[0] and area[1] > mouse_pos[0]:
							x = i
						if area[0] < mouse_pos[1] and area[1] > mouse_pos[1]:
							y = i
						i += 1
					if x != -1 and y != -1:
						for pa in turn_pawns:
							if en == []:  # jesli nie ma szacha
								pa.mv, pa.att = pa.possible_moves(game_window, board, w_destroyed, b_destroyed)
							p = board.pos_matrix[pa.pos[0]][pa.pos[1]]
							if (x, y) == pa.pos:
								hold = 1
								hw = pa
								break
				click += 1
			# kiedy puszczam figure
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1  and turn==player_color:
				if add_button.rect.collidepoint(event.pos):
					adding=True
					if en!=[]:
						check_add=add_defence(count_w, count_b, board, turn, en, turn_pawns, game_window, white_pawns, black_pawns, w_destroyed, b_destroyed)
						if check_txt=="Szach_Mat!" and check_add!=[]:
							check_txt=""
			if click != 0 and pygame.mouse.get_pressed()[0] == False:
				click = 0
				if hold == 1:  # jesli trzymalem figure
					mouse_pos = pygame.mouse.get_pos()
					x = 0
					y = 0
					i = 0
					for area in board.pos_areas():
						if area[0] < mouse_pos[0] and area[1] > mouse_pos[0]:
							x = i
						if area[0] < mouse_pos[1] and area[1] > mouse_pos[1]:
							y = i
						i += 1
					if [x, y] in hw.att:
						old_pos=hw.pos
						hw.pos = (x, y)
						destroy_enemy((x, y), turn, white_pawns, black_pawns, w_destroyed, b_destroyed)
						check = False
						if turn == "white":
							turn = "black"
							turn_pawns = black_pawns
							turn_txt = "Tura czarnych"
							black_watch.resume()
							white_watch.pause_timer()
						else:
							turn = "white"
							turn_pawns = white_pawns
							turn_txt = "Tura białych"
							white_watch.resume()
							black_watch.pause_timer()
						check_txt = ""
						if hw.type == "pawn" and ((hw.color == "w" and hw.pos[1] == 0) or (hw.color == "b" and hw.pos[1] == 7)):
							transform = True
							tr = hw
							t_type="attack"
						if transform == False:
							send(f"@attack {old_pos} {[x, y]}")
							if player_color=="white":
								send(f"@time {white_watch.remaining_time}")
							else:
								send(f"@time {black_watch.remaining_time}")   
					elif [x, y] in hw.mv:
						old_pos=hw.pos
						hw.pos = (x, y)
						check = False
						if turn == "white":
							turn = "black"
							turn_pawns = black_pawns
							turn_txt = "Tura czarnych"
							black_watch.resume()
							white_watch.pause_timer()
						else:
							turn = "white"
							turn_pawns = white_pawns
							turn_txt = "Tura białych"
							white_watch.resume()
							black_watch.pause_timer()
						check_txt = ""
						if hw.type == "pawn" and ((hw.color == "w" and hw.pos[1] == 0) or (hw.color == "b" and hw.pos[1] == 7)):
							transform = True
							tr = hw
							t_type="move"
						if transform == False:
							send(f"@move {old_pos} {[x, y]}")
							if player_color=="white":
								send(f"@time {white_watch.remaining_time}")
							else:
								send(f"@time {black_watch.remaining_time}")  
							
				hold = 0
				hw = 0
		# kiedy trzymam figure
		if hold == 1:
			green_moves = []
			attack_moves = []
			for x in hw.mv:
				green_moves.append(move_rect(x, board.area))
			for x in hw.att:
				attack_moves.append(move_rect(x, board.area))
			for m in green_moves:
				m.draw_moves(game_window, board)
			for a in attack_moves:
				a.draw_attack(game_window, board)
			mouse_pos = pygame.mouse.get_pos()
			hw.mouse_dragging(game_window, mouse_pos)
		chat.draw(game_window)
		first_frame = False

		pygame.display.update()		
		
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
						white_rect=color_rects((res[0]/4+txt_players_width*2, res[1]/10*3), [res[1]/20, res[1]/20], 0)
						black_rect=color_rects((res[0]/4+txt_players_width*2, res[1]/10*4), [res[1]/20, res[1]/20], 1)
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
				i+=1
				print(txt_nicks)
		if new_msg!=[]:
			chat.update_chat(new_msg)
			new_msg.clear()
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
						if white_rect.status==0:
							pl_color="white"
							op_color="black"
						else:
							pl_color="black"
							op_color="white"
						print(nick_box.text, pl_color, ":)h")
						send(f"@gamestart {op_color}")
						kings_chess_online(win, res, nick_box.text, pl_color, new_msg, chat.converted_msgs)
					else:
						send("@chat Potrzeba 2 graczy aby wystartować")
				if white_rect.frame.collidepoint(event.pos) or black_rect.frame.collidepoint(event.pos):
					if white_rect.status==0:
						white_rect.status=1
						black_rect.status=0
					else:
						white_rect.status=0
						black_rect.status=1
			elif event.type == pygame.KEYDOWN:
				if chat.chat_input.status==1:
					if event.key==13:
						if len(chat.chat_input.text)>0:
							send("@chat "+chat.chat_input.text)
							chat.chat_input.text=""
					else:
						chat.chat_input.write(event.key, numpad_keys)
		for x in txt_nicks:
			win.blit(x[0],x[1])
		chat.draw(win)
		start_button.draw(win)
		white_rect.draw(win)
		if len(nicks)==2:
			black_rect.draw(win)
		pygame.display.update()
	while connected==1: #Wersja lobby dla dołączającego gracza
		win.fill((90,200,210))
		win.blit(waiting_txt, waiting_txt_pos)
		if new_msg!=[]:
			chat.update_chat(new_msg)
			for x in new_msg:
				if x=="<SERVER>: Server został wyłączony.":
					connected=0
				if "@gamestart" in x and "@chat" not in x:
					pl_color=x.split()[2]
					print(nick_box.text, pl_color, ":)")
					kings_chess_online(win, res, nick_box.text, pl_color, new_msg, chat.converted_msgs)
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
							send("@chat "+chat.chat_input.text)
							chat.chat_input.text=""
					else:
						chat.chat_input.write(event.key, numpad_keys)
		chat.draw(win)
		pygame.display.update()

	