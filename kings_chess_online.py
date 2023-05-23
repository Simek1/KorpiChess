import pygame
import sys
import copy
import time
from pygame.locals import *
from server import *
from client import *
from online_lobby import *

def kings_chess_online(game_window, res, player_color, msgs, chat_history):
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
	
	add_button = button([board.res[0]+15, (board.res[1]/6)*5],
						[20, 50], (205, 202, 203), text="Dodaj figurę")
	
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
							send('\transform{t_type} {old_pos} {tr.pos} "rook"')
						elif knight_w_button.rect.collidepoint(event.pos) and b_destroyed["knight"]>0:
							b_destroyed["knight"]-=1
							tr.transform("knight", knight_w_png)
							transform=False
							send('\transform{t_type} {old_pos} {tr.pos} "knight"')
						elif bishop_w_button.rect.collidepoint(event.pos) and b_destroyed["bishop"]>0:
							b_destroyed["bishop"]-=1
							tr.transform("bishop", bishop_w_png)
							transform=False
							send('\transform{t_type} {old_pos} {tr.pos} "bishop"')
						elif queen_w_button.rect.collidepoint(event.pos) and b_destroyed["queen"]>0:
							b_destroyed["queen"]-=1
							tr.transform("queen", queen_w_png)
							transform=False
							send('\transform{t_type} {old_pos} {tr.pos} "queen"')
					else:
						if rook_b_button.rect.collidepoint(event.pos) and w_destroyed["rook"]>0:
							w_destroyed["rook"]-=1
							tr.transform("rook", rook_b_png)
							transform=False
							send('\transform{t_type} {old_pos} {tr.pos} "rook"')
						elif knight_b_button.rect.collidepoint(event.pos) and w_destroyed["knight"]>0:
							w_destroyed["knight"]-=1
							tr.transform("knight", knight_b_png)
							transform=False
							send('\transform{t_type} {old_pos} {tr.pos} "knight"')
						elif bishop_b_button.rect.collidepoint(event.pos) and w_destroyed["bishop"]>0:
							w_destroyed["bishop"]-=1
							tr.transform("bishop", bishop_b_png)
							transform=False
							send('\transform{t_type} {old_pos} {tr.pos} "bishop"')
						elif queen_b_button.rect.collidepoint(event.pos) and w_destroyed["queen"]>0:
							w_destroyed["queen"]-=1
							tr.transform("queen", queen_b_png)
							transform=False
							send('\transform{t_type} {old_pos} {tr.pos} "queen"')
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
					elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and turn==player_color: #Sprawdzenie która figura została wybrana
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
			for x in msgs: #dorobic dzialania typu transformacja i sprawdzanie szacha
				if "\chat" not in x:
					if "\move" in x:
						apos=x.split()[2]
						mve=x.split()[3]
					if "\attack" in x:
						apos=x.split()[2]
						mve=x.split()[3]
					if "\transformattack" in x:
						apos=x.split()[2]
						mve=x.split()[3]
						fig=x.split[4]
					if "\transformmove" in x:
						apos=x.split()[2]
						mve=x.split()[3]
						fig=x.split[4]
					if "\time" in x:
						pass
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
			if pygame.mouse.get_pressed()[0]:
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
			if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
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
							send(f"\attack {old_pos} {[x, y]}")
							en = is_check(turn, white_pawns, black_pawns, board, game_window, w_destroyed, b_destroyed)
							if en != []:  # blokowanie ruchow gdy jest szach
								# aktualizacja pozycji na pawn_matrix aby poprawnie sprwadzić możliwe ruchy przy szachu
								for white_pawn in white_pawns:
									white_pawn.draw(game_window, board)
								for black_pawn in black_pawns:
									black_pawn.draw(game_window, board)
								check_txt=is_mat(en, turn, white_pawns, black_pawns, board, game_window, w_destroyed, b_destroyed)
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
							send(f"\move {old_pos} {[x, y]}")
							en = is_check(turn, white_pawns, black_pawns, board, game_window, w_destroyed, b_destroyed)
							if en != []:  # blokowanie ruchow gdy jest szach
								# aktualizacja pozycji na pawn_matrix aby poprawnie sprwadzić możliwe ruchy przy szachu
								for white_pawn in white_pawns:
									white_pawn.draw(game_window, board)
								for black_pawn in black_pawns:
									black_pawn.draw(game_window, board)
								check_txt=is_mat(en, turn, white_pawns, black_pawns, board, game_window, w_destroyed, b_destroyed)
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
		chat.draw(win)
		first_frame = False

		pygame.display.update()