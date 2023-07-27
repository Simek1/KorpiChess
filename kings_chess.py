import pygame
import sys
import copy
import time
from pygame.locals import *
from server import *
from client import *
import copy
#pygame.init()

#res = (800, 600)


#game_window = pygame.display.set_mode(res)
#pygame.display.set_caption("Chess")


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


class ch_board(object):
	def __init__(self, graph, pos, board_resolution):
		self.pos = pos
		self.graph = graph
		self.res = board_resolution
		self.area = self.res[0]/8
		self.pos_matrix = self.positions()
		self.area_table = self.pos_areas()
		self.pawns_matrix = [[0 for x in range(0, 8)] for x in range(0, 8)]

	def positions(self):
		pos_m = []
		row = []
		c = 0
		r = 0
		while r <= self.res[0]-self.area:
			row.append([r+self.pos[0], c+self.pos[1]])
			c += self.area
			if c > self.res[0]-self.area:
				c = 0
				r += self.area
				pos_m.append(row)
				row = []
		return(pos_m)

	def change_res(self, board_resolution):
		pass

	def pos_areas(self):
		table = []
		x = 0
		for i in range(0, 8):
			table.append([x, x+self.area])
			x += self.area
		return(table)
	def add_positions(self, white_pawns, black_pawns, turn, pawn, w_destroyed, b_destroyed, game_window):
		positions=[]
		en_king=[]
		king_pos=[-1,-1]
		if turn=="white":
			for x in black_pawns:
				if x.type=="king":
					king_pos=x.pos
		else:
			for x in white_pawns:
				if x.type=="king":
					king_pos=x.pos
		x=0
		for row in self.pawns_matrix:
			y=0
			for column in row:
				if column==0 and [x,y] not in en_king:
					positions.append([y,x])
				y+=1
			x+=1
		pos_temp=positions.copy()
		for x in pos_temp:
			pawn.pos=x
			self.pawns_matrix[x[1]][x[0]]=pawn.color
			if list(king_pos) in pawn.possible_moves(game_window, self, w_destroyed, b_destroyed)[1]:
				positions.remove(x)
			self.pawns_matrix[x[1]][x[0]]=0
			pawn.pos=(-1,-1)
		if pawn.type=="pawn":
			pos_temp=positions.copy()
			for x in pos_temp:
				if x[1]==0 or x[1]==7:
					positions.remove(x)
			
		return positions
	def append_figure(self, pawn, pos, w_pawns, b_pawns):
		pawn.pos=pos
		x=pos[0]
		y=pos[1]
		if pawn.color=="w":
			w_pawns.append(pawn)
			self.pawns_matrix[y][x]="w"
		else:
			b_pawns.append(pawn)
			self.pawns_matrix[y][x]="b"
	def draw(self, win):
		win.blit(self.graph, self.pos)


class pawn(object):
	def __init__(self, graph, board_pos, pawn_resolution, pawn_type, color):
		self.pos = board_pos
		self.old_pos = self.pos
		self.graph = graph
		self.res = pawn_resolution
		self.type = pawn_type
		self.color = color
		self.att = []
		self.mv = []

	def possible_moves(self, win, board, w_destroyed, b_destroyed):
		possible_attack = []
		possible_positions = []
		if self.type == "king":
			moves = [[self.pos[0]-1, self.pos[1]-1],
					 [self.pos[0]+1, self.pos[1]-1],
					 [self.pos[0]-1, self.pos[1]+1],
					 [self.pos[0]+1, self.pos[1]+1],
					 [self.pos[0], self.pos[1]-1],
					 [self.pos[0]-1, self.pos[1]],
					 [self.pos[0]+1, self.pos[1]],
					 [self.pos[0], self.pos[1]+1]]
			for x in moves:
				if x[0] < 8 and x[0] > -1 and x[1] < 8 and x[1] > -1:
					if board.pawns_matrix[x[1]][x[0]] == 0:
						possible_positions.append(x)
					if board.pawns_matrix[x[1]][x[0]] != 0 and board.pawns_matrix[x[1]][x[0]] != self.color:
						possible_attack.append(x)
		if self.type == "knight":
			moves = [[self.pos[0]-1, self.pos[1]+2],
					 [self.pos[0]+1, self.pos[1]+2],
					 [self.pos[0]-1, self.pos[1]-2],
					 [self.pos[0]+1, self.pos[1]-2],
					 [self.pos[0]-2, self.pos[1]+1],
					 [self.pos[0]-2, self.pos[1]-1],
					 [self.pos[0]+2, self.pos[1]-1],
					 [self.pos[0]+2, self.pos[1]+1]]
			for x in moves:
				if x[0] < 8 and x[0] > -1 and x[1] < 8 and x[1] > -1:
					if board.pawns_matrix[x[1]][x[0]] == 0:
						possible_positions.append(x)
					if board.pawns_matrix[x[1]][x[0]] != 0 and board.pawns_matrix[x[1]][x[0]] != self.color:
						possible_attack.append(x)
		if self.type == "rook":
			# print(self.pos)
			move_up = [x for x in range(self.pos[1]-1, -1, -1)]
			move_down = [x for x in range(self.pos[1]+1, 8)]
			move_right = [x for x in range(self.pos[0]+1, 8)]
			move_left = [x for x in range(self.pos[0]-1, -1, -1)]
			#print(move_up, move_down,move_right,move_left)
			# naprawa
			for x in move_up:
				if board.pawns_matrix[x][self.pos[0]] == 0:
					possible_positions.append([self.pos[0], x])
				elif board.pawns_matrix[x][self.pos[0]] != 0 and board.pawns_matrix[x][self.pos[0]] != self.color:
					possible_attack.append([self.pos[0], x])
					break
				else:
					break
			for x in move_down:
				if board.pawns_matrix[x][self.pos[0]] == 0:
					possible_positions.append([self.pos[0], x])
				elif board.pawns_matrix[x][self.pos[0]] != 0 and board.pawns_matrix[x][self.pos[0]] != self.color:
					possible_attack.append([self.pos[0], x])
					break
				else:
					break
			for x in move_right:
				if board.pawns_matrix[self.pos[1]][x] == 0:
					possible_positions.append([x, self.pos[1]])
				elif board.pawns_matrix[self.pos[1]][x] != 0 and board.pawns_matrix[self.pos[1]][x] != self.color:
					possible_attack.append([x, self.pos[1]])
					break
				else:
					break
			for x in move_left:
				if board.pawns_matrix[self.pos[1]][x] == 0:
					possible_positions.append([x, self.pos[1]])
				elif board.pawns_matrix[self.pos[1]][x] != 0 and board.pawns_matrix[self.pos[1]][x] != self.color:
					possible_attack.append([x, self.pos[1]])
					break
				else:
					break
		if self.type == "bishop":
			move_up = [x for x in range(self.pos[1]-1, -1, -1)]
			move_down = [x for x in range(self.pos[1]+1, 8)]
			move_right = [x for x in range(self.pos[0]+1, 8)]
			move_left = [x for x in range(self.pos[0]-1, -1, -1)]
			move_up_left = [[move_left[i], move_up[i]]
							for i in range(0, min([len(move_up), len(move_left)]))]
			move_up_right = [[move_right[i], move_up[i]]
							 for i in range(0, min([len(move_up), len(move_right)]))]
			move_down_left = [[move_left[i], move_down[i]]
							  for i in range(0, min([len(move_down), len(move_left)]))]
			move_down_right = [[move_right[i], move_down[i]]
							   for i in range(0, min([len(move_down), len(move_right)]))]
			for x in move_up_left:
				if board.pawns_matrix[x[1]][x[0]] == 0:
					possible_positions.append([x[0], x[1]])
				elif board.pawns_matrix[x[1]][x[0]] != 0 and board.pawns_matrix[x[1]][x[0]] != self.color:
					possible_attack.append([x[0], x[1]])
					break
				else:
					break
			for x in move_up_right:
				if board.pawns_matrix[x[1]][x[0]] == 0:
					possible_positions.append([x[0], x[1]])
				elif board.pawns_matrix[x[1]][x[0]] != 0 and board.pawns_matrix[x[1]][x[0]] != self.color:
					possible_attack.append([x[0], x[1]])
					break
				else:
					break
			for x in move_down_left:
				if board.pawns_matrix[x[1]][x[0]] == 0:
					possible_positions.append([x[0], x[1]])
				elif board.pawns_matrix[x[1]][x[0]] != 0 and board.pawns_matrix[x[1]][x[0]] != self.color:
					possible_attack.append([x[0], x[1]])
					break
				else:
					break
			for x in move_down_right:
				if board.pawns_matrix[x[1]][x[0]] == 0:
					possible_positions.append([x[0], x[1]])
				elif board.pawns_matrix[x[1]][x[0]] != 0 and board.pawns_matrix[x[1]][x[0]] != self.color:
					possible_attack.append([x[0], x[1]])
					break
				else:
					break
		if self.type == "queen":
			move_up = [x for x in range(self.pos[1]-1, -1, -1)]
			move_down = [x for x in range(self.pos[1]+1, 8)]
			move_right = [x for x in range(self.pos[0]+1, 8)]
			move_left = [x for x in range(self.pos[0]-1, -1, -1)]
			move_up_left = [[move_left[i], move_up[i]]
							for i in range(0, min([len(move_up), len(move_left)]))]
			move_up_right = [[move_right[i], move_up[i]]
							 for i in range(0, min([len(move_up), len(move_right)]))]
			move_down_left = [[move_left[i], move_down[i]]
							  for i in range(0, min([len(move_down), len(move_left)]))]
			move_down_right = [[move_right[i], move_down[i]]
							   for i in range(0, min([len(move_down), len(move_right)]))]
			for x in move_up:
				if board.pawns_matrix[x][self.pos[0]] == 0:
					possible_positions.append([self.pos[0], x])
				elif board.pawns_matrix[x][self.pos[0]] != 0 and board.pawns_matrix[x][self.pos[0]] != self.color:
					possible_attack.append([self.pos[0], x])
					break
				else:
					break
			for x in move_down:
				if board.pawns_matrix[x][self.pos[0]] == 0:
					possible_positions.append([self.pos[0], x])
				elif board.pawns_matrix[x][self.pos[0]] != 0 and board.pawns_matrix[x][self.pos[0]] != self.color:
					possible_attack.append([self.pos[0], x])
					break
				else:
					break
			for x in move_right:
				if board.pawns_matrix[self.pos[1]][x] == 0:
					possible_positions.append([x, self.pos[1]])
				elif board.pawns_matrix[self.pos[1]][x] != 0 and board.pawns_matrix[self.pos[1]][x] != self.color:
					possible_attack.append([x, self.pos[1]])
					break
				else:
					break
			for x in move_left:
				if board.pawns_matrix[self.pos[1]][x] == 0:
					possible_positions.append([x, self.pos[1]])
				elif board.pawns_matrix[self.pos[1]][x] != 0 and board.pawns_matrix[self.pos[1]][x] != self.color:
					possible_attack.append([x, self.pos[1]])
					break
				else:
					break
			for x in move_up_left:
				if board.pawns_matrix[x[1]][x[0]] == 0:
					possible_positions.append([x[0], x[1]])
				elif board.pawns_matrix[x[1]][x[0]] != 0 and board.pawns_matrix[x[1]][x[0]] != self.color:
					possible_attack.append([x[0], x[1]])
					break
				else:
					break
			for x in move_up_right:
				if board.pawns_matrix[x[1]][x[0]] == 0:
					possible_positions.append([x[0], x[1]])
				elif board.pawns_matrix[x[1]][x[0]] != 0 and board.pawns_matrix[x[1]][x[0]] != self.color:
					possible_attack.append([x[0], x[1]])
					break
				else:
					break
			for x in move_down_left:
				if board.pawns_matrix[x[1]][x[0]] == 0:
					possible_positions.append([x[0], x[1]])
				elif board.pawns_matrix[x[1]][x[0]] != 0 and board.pawns_matrix[x[1]][x[0]] != self.color:
					possible_attack.append([x[0], x[1]])
					break
				else:
					break
			for x in move_down_right:
				if board.pawns_matrix[x[1]][x[0]] == 0:
					possible_positions.append([x[0], x[1]])
				elif board.pawns_matrix[x[1]][x[0]] != 0 and board.pawns_matrix[x[1]][x[0]] != self.color:
					possible_attack.append([x[0], x[1]])
					break
				else:
					break
		if self.type == "pawn":
			if self.color == "w":
				if self.pos[1]-1 > -1:
					if board.pawns_matrix[self.pos[1]-1][self.pos[0]] == 0:
						if self.pos[1]-1==0:
							for dst in w_destroyed:
								if w_destroyed[dst]!=0 and dst!="pawn":
									possible_positions.append([self.pos[0], self.pos[1]-1])
									break
						else:
							possible_positions.append([self.pos[0], self.pos[1]-1])
					if self.pos[0]-1 > -1:
						if board.pawns_matrix[self.pos[1]-1][self.pos[0]-1] != 0 and board.pawns_matrix[self.pos[1]-1][self.pos[0]-1] != self.color:
							if self.pos[1]-1==0:
								for dst in w_destroyed:
									if w_destroyed[dst]!=0 and dst!="pawn":
										possible_attack.append([self.pos[0]-1, self.pos[1]-1])
										break
							else:
								possible_attack.append([self.pos[0]-1, self.pos[1]-1])
					if self.pos[0]+1 < 8:
						if board.pawns_matrix[self.pos[1]-1][self.pos[0]+1] != 0 and board.pawns_matrix[self.pos[1]-1][self.pos[0]+1] != self.color:
							if self.pos[1]-1==0:
								for dst in w_destroyed:
									if w_destroyed[dst]!=0 and dst!="pawn":
										possible_attack.append([self.pos[0]+1, self.pos[1]-1])
										break
							else:
								possible_attack.append([self.pos[0]+1, self.pos[1]-1])
			if self.color == "b":
				if self.pos[1]+1 < 8:
					if board.pawns_matrix[self.pos[1]+1][self.pos[0]] == 0:
						if self.pos[1]+1==7:
							for dst in b_destroyed:
								if b_destroyed[dst]!=0 and dst!="pawn":
									possible_positions.append([self.pos[0], self.pos[1]+1])
									break
						else:
							possible_positions.append([self.pos[0], self.pos[1]+1])
					if self.pos[0]-1 > -1:
						if board.pawns_matrix[self.pos[1]+1][self.pos[0]-1] != 0 and board.pawns_matrix[self.pos[1]+1][self.pos[0]-1] != self.color:
							if self.pos[1]+1==7:
								for dst in b_destroyed:
									if b_destroyed[dst]!=0 and dst!="pawn":
										possible_attack.append([self.pos[0]-1, self.pos[1]+1])
										break
							else:
								possible_attack.append([self.pos[0]-1, self.pos[1]+1])
					if self.pos[0]+1 < 8:
						if board.pawns_matrix[self.pos[1]+1][self.pos[0]+1] != 0 and board.pawns_matrix[self.pos[1]+1][self.pos[0]+1] != self.color:
							if self.pos[1]+1==7:
								for dst in b_destroyed:
									if b_destroyed[dst]!=0 and dst!="pawn":
										possible_attack.append([self.pos[0]+1, self.pos[1]+1])
										break
							else:
								possible_attack.append([self.pos[0]+1, self.pos[1]+1])

		return(possible_positions, possible_attack)

	def transform(self, pawn_type, graph):
		self.graph = graph
		self.type = pawn_type

	def mouse_dragging(self, win, mouse_position, pawn_res):
		temp = copy.copy(self.graph)
		temp.set_alpha(100)
		x=mouse_position[0]-pawn_res[0]/2
		y=mouse_position[1]-pawn_res[1]/2
		win.blit(temp, (x,y))

	def draw(self, win, board):
		board.pawns_matrix[self.pos[1]][self.pos[0]] = self.color
		win.blit(self.graph, board.pos_matrix[self.pos[0]][self.pos[1]])
		if self.old_pos != self.pos:
			board.pawns_matrix[self.old_pos[1]][self.old_pos[0]] = 0
		self.old_pos = self.pos



class move_rect(object):
	def __init__(self, board_pos, board_area):
		self.pos = board_pos
		self.area = board_area
		self.move_color = (33, 245, 68)
		self.attack_color = (255, 0, 0)
		#self.surface=pygame.Surface((board_area, board_area), pygame.SRCALPHA)

	def draw_moves(self, win, board):
		pos = board.pos_matrix[self.pos[0]][self.pos[1]]
		pygame.draw.rect(win, self.move_color, pygame.Rect(
			pos[0], pos[1], self.area, self.area), 2)

	def draw_attack(self, win, board):
		pos = board.pos_matrix[self.pos[0]][self.pos[1]]
		pygame.draw.rect(win, self.attack_color, pygame.Rect(
			pos[0], pos[1], self.area, self.area), 2)


class stopwatch(object):
	def __init__(self, color, font, max_time):
		self.time = max_time
		self.remaining_time = 1
		self.start = pygame.time.get_ticks()
		self.font=font
		self.paused = False
		if color == "w":
			self.color = "Czas białych: "
		else:
			self.color = "Czas czarnych: "
		splited=str(self.time/60).split(".")
		self.txt = self.color+splited[0]+":"+splited[1]

	def update(self, win, board):
		if self.paused == False:
			seconds = (pygame.time.get_ticks() - self.start) // 1000
			self.remaining_time = self.time - seconds
			minutes = int(self.remaining_time/60)
			sec = int(self.remaining_time % 60)
			self.txt = self.color+str(minutes)+":"+str(sec)[:2]
		if self.color == "Czas białych: ":
			win.blit(self.font.render(self.txt, True, (0, 0, 0)),
					 (board.res[0]+15+board.pos[0], board.res[1]/4+board.pos[1]))
		else:
			win.blit(self.font.render(self.txt, True, (0, 0, 0)),
					 (board.res[0]+15+board.pos[0], board.res[1]/4+40+board.pos[1]))

	def pause_timer(self):
		self.paused = True
		self.pause = pygame.time.get_ticks()

	def resume(self):
		self.paused = False
		self.start += pygame.time.get_ticks()-self.pause


class button(object):
	def __init__(self, pos, size, color, text="", undertext="", graph="", figure=""):
		self.pos = pos
		self.size = size
		self.color = color
		self.text = text
		self.graph = graph
		self.undertext = undertext
		self.font_size = int(self.size[0])
		self.undertext_font=pygame.font.SysFont("arial", int(self.font_size/4))
		self.font = pygame.font.SysFont("arial", self.font_size)
		self.rect = pygame.Rect(
			self.pos[0], self.pos[1], self.size[0], self.size[1])
		if self.graph != "" and type(self.graph) != pygame.Surface:
			self.graph.transform.scale(self.graph, self.size)
		self.figure=figure
	def draw(self, win):
		txt = self.font.render(self.text, True, (0, 0, 0))
		txt_rect = txt.get_rect()
		if self.size[0] < txt_rect.width:
			self.size[0] = txt_rect.width+20
			self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
		if self.graph == "":
			pygame.draw.rect(win, self.color, self.rect)
		else:
			win.blit(self.graph, (self.pos[0], self.pos[1]))
		win.blit(txt, (int(self.pos[0]+self.size[0]/2-txt_rect.width/2),
				 int(self.pos[1]+self.size[1]/2-txt_rect.height/2)))
		if self.undertext != "":
			undertxt = self.undertext_font.render(self.undertext, True, (0, 0, 0))
			undertxt_rect = undertxt.get_rect()
			win.blit(undertxt, (int(self.pos[0]+self.size[0]/2-undertxt_rect.width/2), int(
				self.pos[1]+self.size[1]+undertxt_rect.height/2)))


class notification(object):
	def __init__(self, pos, size, color, text, font_size, frame_color=""):
		self.pos = pos
		self.size = size
		self.color = color
		self.text = text
		self.font_size=font_size
		self.font = pygame.font.SysFont("arial", self.font_size)
		self.frame_color = frame_color
		self.rect = pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

	def draw(self, win):
		txt = self.font.render(self.text, True, (0, 0, 0))
		txt_rect = txt.get_rect()
		if self.frame_color == "":
			self.frame_color = (0, 0, 0)
		pygame.draw.rect(win, self.color, self.rect)
		pygame.draw.rect(win, self.frame_color, self.rect, 5)
		win.blit(txt, (int(self.pos[0]+self.size[0]/2-txt_rect.width/2), int(self.pos[1]+self.size[1]/5-txt_rect.height/2)))


'''
def end_turn(turn, turn_pawns, white_pawns, black_pawns, turn_txt, white_watch, black_watch): #nie dziala bo zmienne nie sa globalne
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
'''

def destroy_enemy(pos, turn, white_pawns, black_pawns, w_destroyed, b_destroyed):
	i = 0
	if turn == "white":
		for pawn in black_pawns:
			if pawn.pos == pos:
				b_destroyed[pawn.type]+=1
				del(black_pawns[i])
				break
			i += 1
	else:
		for pawn in white_pawns:
			if pawn.pos == pos:
				w_destroyed[pawn.type]+=1
				del(white_pawns[i])
				break
			i += 1


def is_check(turn, white_pawns, black_pawns, board, game_window, w_destroyed, b_destroyed):
	enemies = []
	if ("king" in [p.type for p in white_pawns]) and ("king" in [p.type for p in black_pawns]):
		if turn == "white":
			for p in white_pawns:
				if p.type == "king":
					king_in_danger = p
					break
			for pawn in black_pawns:
				att = pawn.possible_moves(game_window, board, w_destroyed, b_destroyed)[1]
				if list(king_in_danger.pos) in att:
					pawn.mv, pawn.att = pawn.possible_moves(game_window, board, w_destroyed, b_destroyed)
					enemies.append(pawn)
		else:
			for p in black_pawns:
				if p.type == "king":
					king_in_danger = p
			for pawn in white_pawns:
				att = pawn.possible_moves(game_window, board, w_destroyed, b_destroyed)[1]
				if list(king_in_danger.pos) in att:
					pawn.mv, pawn.att = pawn.possible_moves(game_window, board, w_destroyed, b_destroyed)
					enemies.append(pawn)

	return(enemies)


def is_mat(enemies, turn, white_pawns, black_pawns, board, game_window, w_destroyed, b_destroyed):
	check_txt = "Szach!"
	if turn == "white":
		for pawn in white_pawns:
			new_mv = []
			new_att = []
			pawn.mv, pawn.att = pawn.possible_moves(game_window, board, w_destroyed, b_destroyed)
			for enemy in enemies:
				if pawn.type == "king":
					# sprawdzenie czy krol moze uciec
					for mv in pawn.mv:
						if mv not in enemy.mv:
							board.pawns_matrix[mv[1]][mv[0]] = "w"
							board.pawns_matrix[pawn.pos[1]][pawn.pos[0]] = 0
							pawn.pos = mv
							possiblity = is_check(turn, white_pawns, black_pawns, board, game_window, w_destroyed, b_destroyed)
							pawn.pos = pawn.old_pos
							board.pawns_matrix[mv[1]][mv[0]] = 0
							board.pawns_matrix[pawn.pos[1]][pawn.pos[0]] = 'w'
							if possiblity == []:
								new_mv.append(mv)

					# sprawdzenie czy krol moze zniszczyc przeciwnika
					if list(enemy.pos) in pawn.att:
						for att in pawn.att:
							if att==list(enemy.pos):
								popped_pawn = black_pawns.pop(black_pawns.index(enemy))
								board.pawns_matrix[popped_pawn.pos[1]][popped_pawn.pos[0]] = "w"
								board.pawns_matrix[pawn.pos[1]][pawn.pos[0]] = 0
								old_pos=pawn.pos
								pawn.pos=(att[0],att[1])
								possiblity = is_check(turn, white_pawns, black_pawns, board, game_window, w_destroyed, b_destroyed)
								pawn.pos=old_pos
								black_pawns.append(popped_pawn)
								board.pawns_matrix[popped_pawn.pos[1]][popped_pawn.pos[0]] = "b"
								board.pawns_matrix[pawn.pos[1]][pawn.pos[0]] = "w"
								if possiblity == []:
									new_att.append(att)
				else:
					# sprawdzenie czy pionek może zasłonić króla
					for mv in pawn.mv:
						if mv in enemy.mv:
							board.pawns_matrix[mv[1]][mv[0]] = "w"
							board.pawns_matrix[pawn.pos[1]][pawn.pos[0]] = 0
							possiblity = is_check(turn, white_pawns, black_pawns, board, game_window, w_destroyed, b_destroyed)
							board.pawns_matrix[mv[1]][mv[0]] = 0
							board.pawns_matrix[pawn.pos[1]][pawn.pos[0]] = 'w'
							if possiblity == []:
								new_mv.append(mv)

					# sprawdzenie czy pionek moze znisczyc przeciwnika
					if list(enemy.pos) in pawn.att:
						for att in pawn.att:
							if att==list(enemy.pos):
								popped_pawn = black_pawns.pop(black_pawns.index(enemy))
								board.pawns_matrix[popped_pawn.pos[1]][popped_pawn.pos[0]] = "w"
								board.pawns_matrix[pawn.pos[1]][pawn.pos[0]] = 0
								possiblity = is_check(turn, white_pawns, black_pawns, board, game_window, w_destroyed, b_destroyed)
								black_pawns.append(popped_pawn)
								board.pawns_matrix[popped_pawn.pos[1]][popped_pawn.pos[0]] = "b"
								board.pawns_matrix[pawn.pos[1]][pawn.pos[0]] = "w"
								if possiblity == []:
									new_att.append(att)
			pawn.mv = new_mv
			pawn.att = new_att
		mat = True
		for pawn in white_pawns:
			if pawn.mv != [] or pawn.att != []:
				mat = False
				break
	else:
		for pawn in black_pawns:
			new_mv = []
			new_att = []
			pawn.mv, pawn.att = pawn.possible_moves(game_window, board, w_destroyed, b_destroyed)
			for enemy in enemies:
				if pawn.type == "king":
					# sprawdzenie czy krol moze uciec
					for mv in pawn.mv:
						if mv not in enemy.mv:
							board.pawns_matrix[mv[1]][mv[0]] = "b"
							board.pawns_matrix[pawn.pos[1]][pawn.pos[0]] = 0
							pawn.pos = mv
							possiblity = is_check(turn, white_pawns, black_pawns, board, game_window, w_destroyed, b_destroyed)
							pawn.pos = pawn.old_pos
							board.pawns_matrix[mv[1]][mv[0]] = 0
							board.pawns_matrix[pawn.pos[1]][pawn.pos[0]] = 'b'
							if possiblity == []:
								new_mv.append(mv)

					# sprawdzenie czy krol moze zniszczyc przeciwnika
					if list(enemy.pos) in pawn.att:
						for att in pawn.att:
							if att==list(enemy.pos):
								popped_pawn=white_pawns.pop(white_pawns.index(enemy))
								board.pawns_matrix[popped_pawn.pos[1]][popped_pawn.pos[0]]="b"
								board.pawns_matrix[pawn.pos[1]][pawn.pos[0]]=0
								old_pos=pawn.pos
								pawn.pos=(att[0],att[1])
								possiblity=is_check(turn, white_pawns, black_pawns, board, game_window, w_destroyed, b_destroyed)
								pawn.pos=old_pos
								white_pawns.append(popped_pawn)
								board.pawns_matrix[popped_pawn.pos[1]][popped_pawn.pos[0]]="w"
								board.pawns_matrix[pawn.pos[1]][pawn.pos[0]]="b"
								if possiblity==[]:
									new_att.append(att)
				else:
					# sprawdzenie czy pionek może zasłonić króla
					for mv in pawn.mv:
						if mv in enemy.mv:
							board.pawns_matrix[mv[1]][mv[0]] = "b"
							board.pawns_matrix[pawn.pos[1]][pawn.pos[0]] = 0
							possiblity = is_check(turn, white_pawns, black_pawns, board, game_window, w_destroyed, b_destroyed)
							board.pawns_matrix[mv[1]][mv[0]] = 0
							board.pawns_matrix[pawn.pos[1]][pawn.pos[0]] = 'b'
							if possiblity == []:
								new_mv.append(mv)

					# sprawdzenie czy pionek moze znisczyc przeciwnika
					if list(enemy.pos) in pawn.att:
						for att in pawn.att: #poprawic ta czesc w oryginalnym trybie
							if att==list(enemy.pos):
								popped_pawn=white_pawns.pop(white_pawns.index(enemy))
								board.pawns_matrix[popped_pawn.pos[1]][popped_pawn.pos[0]]="b"
								board.pawns_matrix[pawn.pos[1]][pawn.pos[0]]=0
								possiblity=is_check(turn, white_pawns, black_pawns, board, game_window, w_destroyed, b_destroyed)
								white_pawns.append(popped_pawn)
								board.pawns_matrix[popped_pawn.pos[1]][popped_pawn.pos[0]]="w"
								board.pawns_matrix[pawn.pos[1]][pawn.pos[0]]="b"
								if possiblity==[]:
									new_att.append(att)
			pawn.mv = new_mv
			pawn.att = new_att
		mat = True
		for pawn in black_pawns:
			if pawn.mv != [] or pawn.att != []:
				mat = False
				break
	if mat:
		check_txt = "Szach-Mat!"
	return check_txt

def add_defence(count_w, count_b, board, turn, enemies, turn_pawns, game_window, white_pawns, black_pawns, w_destroyed, b_destroyed): #Sprawdzenie czy mozna wybronic mata dodaniem nowego pionka
	add_mv=[]
	for x in turn_pawns:
		if x.type=="king":
			king=x
			break
	if turn=="white":
		count=0
		for x in count_w:
			if count_w[x]!=0:
				count=1
				break
		if count==0: #nie mozna postawic nowych pionkow
			pass
		else:
			for enemy in enemies:
				for mv in enemy.mv:
					if tuple(mv)!=king.pos:
						board.pawns_matrix[mv[1]][mv[0]] = "w"
						possiblity = is_check(turn, white_pawns, black_pawns, board, game_window, w_destroyed, b_destroyed)
						board.pawns_matrix[mv[1]][mv[0]] = 0
						if possiblity == []:
							add_mv.append(mv)
	else:
		count=0
		for x in count_w:
			if count_w[x]!=0:
				count=1
				break
		if count==0: #nie mozna postawic nowych pionkow
			pass
		else:
			for enemy in enemies:
				for mv in enemy.mv:
					if tuple(mv)!=king.pos:
						board.pawns_matrix[mv[1]][mv[0]] = "b"
						possiblity = is_check(turn, white_pawns, black_pawns, board, game_window, w_destroyed, b_destroyed)
						board.pawns_matrix[mv[1]][mv[0]] = 0
						if possiblity == []:
							add_mv.append(mv)
	return add_mv
	
def kings_chess(game_window, res, timers, max_time):
	res_b = (res[1]-res[1]/5-res[1]/50, res[1]-res[1]/5-res[1]/50)
	bg_color = (185, 182, 183)
	
	font_size = int(game_window.get_size()[0]/45)
	font = pygame.font.SysFont("arial", font_size)
	
	board_png = pygame.image.load('images/board.png')
	board_png = pygame.transform.scale(board_png, res_b)

	org_pawn_b_png = pygame.image.load('images/pawn_b.png')
	org_pawn_w_png = pygame.image.load('images/pawn_w.png')
	org_king_b_png = pygame.image.load('images/king_b.png')
	org_king_w_png = pygame.image.load('images/king_w.png')
	org_queen_b_png = pygame.image.load('images/queen_b.png')
	org_queen_w_png = pygame.image.load('images/queen_w.png')
	org_bishop_b_png = pygame.image.load('images/bishop_b.png')
	org_bishop_w_png = pygame.image.load('images/bishop_w.png')
	org_knight_b_png = pygame.image.load('images/knight_b.png')
	org_knight_w_png = pygame.image.load('images/knight_w.png')
	org_rook_b_png = pygame.image.load('images/rook_b.png')
	org_rook_w_png = pygame.image.load('images/rook_w.png')

	pawn_res = int(res_b[0]/8)
	pawn_res = (pawn_res, pawn_res)

	pawn_b_png = pygame.transform.scale(org_pawn_b_png, pawn_res)
	pawn_w_png = pygame.transform.scale(org_pawn_w_png, pawn_res)
	king_b_png = pygame.transform.scale(org_king_b_png, pawn_res)
	king_w_png = pygame.transform.scale(org_king_w_png, pawn_res)
	queen_b_png = pygame.transform.scale(org_queen_b_png, pawn_res)
	queen_w_png = pygame.transform.scale(org_queen_w_png, pawn_res)
	bishop_b_png = pygame.transform.scale(org_bishop_b_png, pawn_res)
	bishop_w_png = pygame.transform.scale(org_bishop_w_png, pawn_res)
	knight_b_png = pygame.transform.scale(org_knight_b_png, pawn_res)
	knight_w_png = pygame.transform.scale(org_knight_w_png, pawn_res)
	rook_b_png = pygame.transform.scale(org_rook_b_png, pawn_res)
	rook_w_png = pygame.transform.scale(org_rook_w_png, pawn_res)
	
	break_font=font.render("Z", True, (0, 0, 0))
	board=ch_board(board_png,(break_font.get_rect().width,0), res_b)
		
	
	# tworzenie okna zmiany pionka
	transform_w = notification([20, 20], [res[0]-40, res[1]/2-20], (185, 182, 183), "Wybierz figurę w którą zamienić pionka", font_size*2)
	
	rook_b_button = button([transform_w.pos[0]+transform_w.size[0]/5-pawn_res[0]/2, transform_w.pos[1]+transform_w.size[1]/2-pawn_res[1]/2], pawn_res, (0, 0, 0), undertext="Wieża", graph=rook_b_png)
	knight_b_button = button([(transform_w.pos[0]+transform_w.size[0]/5-pawn_res[0]/2)*2, transform_w.pos[1]+transform_w.size[1]/2-pawn_res[1]/2], pawn_res, (0, 0, 0), undertext="Koń", graph=knight_b_png)
	bishop_b_button = button([(transform_w.pos[0]+transform_w.size[0]/5-pawn_res[0]/2)*3, transform_w.pos[1]+transform_w.size[1]/2-pawn_res[1]/2], pawn_res, (0, 0, 0), undertext="Goniec", graph=bishop_b_png)
	queen_b_button = button([(transform_w.pos[0]+transform_w.size[0]/5-pawn_res[0]/2)*4, transform_w.pos[1]+transform_w.size[1]/2-pawn_res[1]/2], pawn_res, (0, 0, 0), undertext="Hetman", graph=queen_b_png)
	
	rook_w_button = button([transform_w.pos[0]+transform_w.size[0]/5-pawn_res[0]/2,transform_w.pos[1]+transform_w.size[1]/2-pawn_res[1]/2], pawn_res, (0, 0, 0), undertext="Wieża", graph=rook_w_png)
	knight_w_button = button([(transform_w.pos[0]+transform_w.size[0]/5-pawn_res[0]/2)*2, transform_w.pos[1]+transform_w.size[1]/2-pawn_res[1]/2], pawn_res, (0, 0, 0), undertext="Koń", graph=knight_w_png)
	bishop_w_button = button([(transform_w.pos[0]+transform_w.size[0]/5-pawn_res[0]/2)*3, transform_w.pos[1]+transform_w.size[1]/2-pawn_res[1]/2], pawn_res, (0, 0, 0), undertext="Goniec", graph=bishop_w_png)
	queen_w_button = button([(transform_w.pos[0]+transform_w.size[0]/5-pawn_res[0]/2)*4, transform_w.pos[1]+transform_w.size[1]/2-pawn_res[1]/2], pawn_res, (0, 0, 0), undertext="Hetman", graph=queen_w_png)
	
	#######
	
	# Tworzenie okna dodawania pionka
	
	add_w = notification([20, 20], [res[0]-40, res[1]/2-20],(185, 182, 183), "Wybierz figurę", font_size*2)
	
	mini_pawn_res=(pawn_res[0]/2,pawn_res[1]/2)
	
	mini_pawn_b_png = pygame.transform.scale(org_pawn_b_png, mini_pawn_res)
	mini_pawn_w_png = pygame.transform.scale(org_pawn_w_png, mini_pawn_res)
	mini_king_b_png = pygame.transform.scale(org_king_b_png, mini_pawn_res)
	mini_king_w_png = pygame.transform.scale(org_king_w_png, mini_pawn_res)
	mini_queen_b_png = pygame.transform.scale(org_queen_b_png, mini_pawn_res)
	mini_queen_w_png = pygame.transform.scale(org_queen_w_png, mini_pawn_res)
	mini_bishop_b_png = pygame.transform.scale(org_bishop_b_png, mini_pawn_res)
	mini_bishop_w_png = pygame.transform.scale(org_bishop_w_png, mini_pawn_res)
	mini_knight_b_png = pygame.transform.scale(org_knight_b_png, mini_pawn_res)
	mini_knight_w_png = pygame.transform.scale(org_knight_w_png, mini_pawn_res)
	mini_rook_b_png = pygame.transform.scale(org_rook_b_png, mini_pawn_res)
	mini_rook_w_png = pygame.transform.scale(org_rook_w_png, mini_pawn_res)
	
	add_rook1_b = button([board.pos[0],res_b[1]+board.pos[1]+break_font.get_rect().height], pawn_res, (0, 0, 0), graph=rook_b_png, figure="rook")
	add_knight1_b = button([res_b[0]/8+board.pos[0], res_b[1]+board.pos[1]+break_font.get_rect().height], pawn_res, (0, 0, 0), graph=knight_b_png, figure="knight")
	add_bishop1_b = button([res_b[0]/8*2+board.pos[0], res_b[1]+board.pos[1]+break_font.get_rect().height], pawn_res, (0, 0, 0), graph=bishop_b_png, figure="bishop")
	add_queen_b = button([res_b[0]/8*3+board.pos[0], res_b[1]+board.pos[1]+break_font.get_rect().height], pawn_res, (0, 0, 0), graph=queen_b_png, figure="queen")
	add_king_b = button([res_b[0]/8*4+board.pos[0], res_b[1]+board.pos[1]+break_font.get_rect().height], pawn_res, (0, 0, 0), graph=king_b_png, figure="king")
	add_bishop2_b = button([res_b[0]/8*5+board.pos[0], res_b[1]+board.pos[1]+break_font.get_rect().height], pawn_res, (0, 0, 0), graph=bishop_b_png, figure="bishop")
	add_knight2_b = button([res_b[0]/8*6+board.pos[0], res_b[1]+board.pos[1]+break_font.get_rect().height], pawn_res, (0, 0, 0), graph=knight_b_png, figure="knight")
	add_rook2_b = button([res_b[0]/8*7+board.pos[0], res_b[1]+board.pos[1]+break_font.get_rect().height], pawn_res, (0, 0, 0), graph=rook_b_png, figure="rook")
	add_pawn1_b = button([board.pos[0],res_b[1]+pawn_res[1]+board.pos[1]+break_font.get_rect().height], pawn_res, (0, 0, 0), graph=pawn_b_png, figure="pawn")
	add_pawn2_b = button([res_b[0]/8+board.pos[0], res_b[1]+pawn_res[1]+board.pos[1]+break_font.get_rect().height], pawn_res, (0, 0, 0), graph=pawn_b_png, figure="pawn")
	add_pawn3_b = button([res_b[0]/8*2+board.pos[0], res_b[1]+pawn_res[1]+board.pos[1]+break_font.get_rect().height], pawn_res, (0, 0, 0), graph=pawn_b_png, figure="pawn")
	add_pawn4_b = button([res_b[0]/8*3+board.pos[0], res_b[1]+pawn_res[1]+board.pos[1]+break_font.get_rect().height], pawn_res, (0, 0, 0), graph=pawn_b_png, figure="pawn")
	add_pawn5_b = button([res_b[0]/8*4+board.pos[0], res_b[1]+pawn_res[1]+board.pos[1]+break_font.get_rect().height], pawn_res, (0, 0, 0), graph=pawn_b_png, figure="pawn")
	add_pawn6_b = button([res_b[0]/8*5+board.pos[0], res_b[1]+pawn_res[1]+board.pos[1]+break_font.get_rect().height], pawn_res, (0, 0, 0), graph=pawn_b_png, figure="pawn")
	add_pawn7_b = button([res_b[0]/8*6+board.pos[0], res_b[1]+pawn_res[1]+board.pos[1]+break_font.get_rect().height], pawn_res, (0, 0, 0), graph=pawn_b_png, figure="pawn")
	add_pawn8_b = button([res_b[0]/8*7+board.pos[0], res_b[1]+pawn_res[1]+board.pos[1]+break_font.get_rect().height], pawn_res, (0, 0, 0), graph=pawn_b_png, figure="pawn")
	
	opp_rook1_b = button([board.pos[0],res_b[1]+board.pos[1]], mini_pawn_res, (0, 0, 0), graph=mini_rook_b_png, figure="rook")
	opp_knight1_b = button([res_b[0]/8+board.pos[0], res_b[1]+board.pos[1]], mini_pawn_res, (0, 0, 0), graph=mini_knight_b_png, figure="knight")
	opp_bishop1_b = button([res_b[0]/8*2+board.pos[0], res_b[1]+board.pos[1]], mini_pawn_res, (0, 0, 0), graph=mini_bishop_b_png, figure="bishop")
	opp_queen_b = button([res_b[0]/8*3+board.pos[0], res_b[1]+board.pos[1]], mini_pawn_res, (0, 0, 0), graph=mini_queen_b_png, figure="queen")
	opp_king_b = button([res_b[0]/8*4+board.pos[0], res_b[1]+board.pos[1]], mini_pawn_res, (0, 0, 0), graph=mini_king_b_png, figure="king")
	opp_bishop2_b = button([res_b[0]/8*5+board.pos[0], res_b[1]+board.pos[1]], mini_pawn_res, (0, 0, 0), graph=mini_bishop_b_png, figure="bishop")
	opp_knight2_b = button([res_b[0]/8*6+board.pos[0], res_b[1]+board.pos[1]], mini_pawn_res, (0, 0, 0), graph=mini_knight_b_png, figure="knight")
	opp_rook2_b = button([res_b[0]/8*7+board.pos[0], res_b[1]+board.pos[1]], mini_pawn_res, (0, 0, 0), graph=mini_rook_b_png, figure="rook")
	opp_pawn1_b = button([board.pos[0],res_b[1]+pawn_res[1]+board.pos[1]], mini_pawn_res, (0, 0, 0), graph=mini_pawn_b_png, figure="pawn")
	opp_pawn2_b = button([res_b[0]/8+board.pos[0], res_b[1]+pawn_res[1]+board.pos[1]], mini_pawn_res, (0, 0, 0), graph=mini_pawn_b_png, figure="pawn")
	opp_pawn3_b = button([res_b[0]/8*2+board.pos[0], res_b[1]+pawn_res[1]+board.pos[1]], mini_pawn_res, (0, 0, 0), graph=mini_pawn_b_png, figure="pawn")
	opp_pawn4_b = button([res_b[0]/8*3+board.pos[0], res_b[1]+pawn_res[1]+board.pos[1]], mini_pawn_res, (0, 0, 0), graph=mini_pawn_b_png, figure="pawn")
	opp_pawn5_b = button([res_b[0]/8*4+board.pos[0], res_b[1]+pawn_res[1]+board.pos[1]], mini_pawn_res, (0, 0, 0), graph=mini_pawn_b_png, figure="pawn")
	opp_pawn6_b = button([res_b[0]/8*5+board.pos[0], res_b[1]+pawn_res[1]+board.pos[1]], mini_pawn_res, (0, 0, 0), graph=mini_pawn_b_png, figure="pawn")
	opp_pawn7_b = button([res_b[0]/8*6+board.pos[0], res_b[1]+pawn_res[1]+board.pos[1]], mini_pawn_res, (0, 0, 0), graph=mini_pawn_b_png, figure="pawn")
	opp_pawn8_b = button([res_b[0]/8*7+board.pos[0], res_b[1]+pawn_res[1]+board.pos[1]], mini_pawn_res, (0, 0, 0), graph=mini_pawn_b_png, figure="pawn")

	black_opp=[opp_rook1_b, opp_knight1_b, opp_bishop1_b, opp_queen_b, opp_king_b, opp_bishop2_b, opp_knight2_b, opp_rook2_b, opp_pawn1_b,
			 opp_pawn2_b, opp_pawn3_b,opp_pawn4_b, opp_pawn5_b, opp_pawn6_b, opp_pawn7_b, opp_pawn8_b]
	start_pos=[res_b[0]+board.pos[0], res[1]/10*5]
	print(start_pos)
	first_pawn=True
	for pw in black_opp:
		if start_pos[0]+mini_pawn_res[0]<res[0] and not (first_pawn==True and pw.figure=="pawn"):
			pw.pos=(start_pos[0], start_pos[1])
			start_pos[0]+=mini_pawn_res[0]
		else:
			if first_pawn==True and pw.figure=="pawn":
				first_pawn=False
			start_pos[0]=res_b[0]+board.pos[0]
			start_pos[1]+=mini_pawn_res[1]
			pw.pos=(start_pos[0], start_pos[1])
			start_pos[0]+=mini_pawn_res[0]
		print(start_pos, pw.pos)
	
	
	black_add_buttons=[add_rook1_b, add_knight1_b, add_bishop1_b, add_queen_b, add_king_b, add_bishop2_b, add_knight2_b, add_rook2_b,
					add_pawn1_b, add_pawn2_b, add_pawn3_b, add_pawn4_b, add_pawn5_b, add_pawn6_b, add_pawn7_b, add_pawn8_b]
	
	
	
	add_rook1_w = button([board.pos[0],res_b[1]+board.pos[1]+break_font.get_rect().height], pawn_res, (0, 0, 0), graph=rook_w_png, figure="rook")
	add_knight1_w = button([res_b[0]/8+board.pos[0], res_b[1]+board.pos[1]+break_font.get_rect().height], pawn_res, (0, 0, 0), graph=knight_w_png, figure="knight")
	add_bishop1_w = button([res_b[0]/8*2+board.pos[0], res_b[1]+board.pos[1]+break_font.get_rect().height], pawn_res, (0, 0, 0), graph=bishop_w_png, figure="bishop")
	add_queen_w = button([res_b[0]/8*3+board.pos[0], res_b[1]+board.pos[1]+break_font.get_rect().height], pawn_res, (0, 0, 0), graph=queen_w_png, figure="queen")
	add_king_w = button([res_b[0]/8*4+board.pos[0], res_b[1]+board.pos[1]+break_font.get_rect().height], pawn_res, (0, 0, 0), graph=king_w_png, figure="king")
	add_bishop2_w = button([res_b[0]/8*5+board.pos[0], res_b[1]+board.pos[1]+break_font.get_rect().height], pawn_res, (0, 0, 0), graph=bishop_w_png, figure="bishop")
	add_knight2_w = button([res_b[0]/8*6+board.pos[0], res_b[1]+board.pos[1]+break_font.get_rect().height], pawn_res, (0, 0, 0), graph=knight_w_png, figure="knight")
	add_rook2_w = button([res_b[0]/8*7+board.pos[0], res_b[1]+board.pos[1]+break_font.get_rect().height], pawn_res, (0, 0, 0), graph=rook_w_png, figure="rook")
	add_pawn1_w = button([board.pos[0],res_b[1]+pawn_res[1]+board.pos[1]+break_font.get_rect().height], pawn_res, (0, 0, 0), graph=pawn_w_png, figure="pawn")
	add_pawn2_w = button([res_b[0]/8+board.pos[0], res_b[1]+pawn_res[1]+board.pos[1]+break_font.get_rect().height], pawn_res, (0, 0, 0), graph=pawn_w_png, figure="pawn")
	add_pawn3_w = button([res_b[0]/8*2+board.pos[0], res_b[1]+pawn_res[1]+board.pos[1]+break_font.get_rect().height], pawn_res, (0, 0, 0), graph=pawn_w_png, figure="pawn")
	add_pawn4_w = button([res_b[0]/8*3+board.pos[0], res_b[1]+pawn_res[1]+board.pos[1]+break_font.get_rect().height], pawn_res, (0, 0, 0), graph=pawn_w_png, figure="pawn")
	add_pawn5_w = button([res_b[0]/8*4+board.pos[0], res_b[1]+pawn_res[1]+board.pos[1]+break_font.get_rect().height], pawn_res, (0, 0, 0), graph=pawn_w_png, figure="pawn")
	add_pawn6_w = button([res_b[0]/8*5+board.pos[0], res_b[1]+pawn_res[1]+board.pos[1]+break_font.get_rect().height], pawn_res, (0, 0, 0), graph=pawn_w_png, figure="pawn")
	add_pawn7_w = button([res_b[0]/8*6+board.pos[0], res_b[1]+pawn_res[1]+board.pos[1]+break_font.get_rect().height], pawn_res, (0, 0, 0), graph=pawn_w_png, figure="pawn")
	add_pawn8_w = button([res_b[0]/8*7+board.pos[0], res_b[1]+pawn_res[1]+board.pos[1]+break_font.get_rect().height], pawn_res, (0, 0, 0), graph=pawn_w_png, figure="pawn")
	
	opp_rook1_w = button([0,res_b[1]], mini_pawn_res, (0, 0, 0), graph=mini_rook_w_png, figure="rook")
	opp_knight1_w = button([res_b[0]/8, res_b[1]], mini_pawn_res, (0, 0, 0), graph=mini_knight_w_png, figure="knight")
	opp_bishop1_w = button([res_b[0]/8*2, res_b[1]], mini_pawn_res, (0, 0, 0), graph=mini_bishop_w_png, figure="bishop")
	opp_queen_w = button([res_b[0]/8*3, res_b[1]], mini_pawn_res, (0, 0, 0), graph=mini_queen_w_png, figure="queen")
	opp_king_w = button([res_b[0]/8*4, res_b[1]], mini_pawn_res, (0, 0, 0), graph=mini_king_w_png, figure="king")
	opp_bishop2_w = button([res_b[0]/8*5, res_b[1]], mini_pawn_res, (0, 0, 0), graph=mini_bishop_w_png, figure="bishop")
	opp_knight2_w = button([res_b[0]/8*6, res_b[1]], mini_pawn_res, (0, 0, 0), graph=mini_knight_w_png, figure="knight")
	opp_rook2_w = button([res_b[0]/8*7, res_b[1]], mini_pawn_res, (0, 0, 0), graph=mini_rook_w_png, figure="rook")
	opp_pawn1_w = button([0,res_b[1]+pawn_res[1]], mini_pawn_res, (0, 0, 0), graph=mini_pawn_w_png, figure="pawn")
	opp_pawn2_w = button([res_b[0]/8, res_b[1]+pawn_res[1]], mini_pawn_res, (0, 0, 0), graph=mini_pawn_w_png, figure="pawn")
	opp_pawn3_w = button([res_b[0]/8*2, res_b[1]+pawn_res[1]], mini_pawn_res, (0, 0, 0), graph=mini_pawn_w_png, figure="pawn")
	opp_pawn4_w = button([res_b[0]/8*3, res_b[1]+pawn_res[1]], mini_pawn_res, (0, 0, 0), graph=mini_pawn_w_png, figure="pawn")
	opp_pawn5_w = button([res_b[0]/8*4, res_b[1]+pawn_res[1]], mini_pawn_res, (0, 0, 0), graph=mini_pawn_w_png, figure="pawn")
	opp_pawn6_w = button([res_b[0]/8*5, res_b[1]+pawn_res[1]], mini_pawn_res, (0, 0, 0), graph=mini_pawn_w_png, figure="pawn")
	opp_pawn7_w = button([res_b[0]/8*6, res_b[1]+pawn_res[1]], mini_pawn_res, (0, 0, 0), graph=mini_pawn_w_png, figure="pawn")
	opp_pawn8_w = button([res_b[0]/8*7, res_b[1]+pawn_res[1]], mini_pawn_res, (0, 0, 0), graph=mini_pawn_w_png, figure="pawn")

	
	white_opp=[opp_rook1_w, opp_knight1_w, opp_bishop1_w, opp_queen_w, opp_king_w, opp_bishop2_w, opp_knight2_w, opp_rook2_w, opp_pawn1_w,
			opp_pawn2_w, opp_pawn3_w, opp_pawn4_w, opp_pawn5_w, opp_pawn6_w, opp_pawn7_w, opp_pawn8_w]
	
	for i in range(len(white_opp)):
		white_opp[i].pos=black_opp[i].pos
	
	white_add_buttons=[add_rook1_w, add_knight1_w, add_bishop1_w, add_queen_w, add_king_w, add_bishop2_w, add_knight2_w, add_rook2_w,
					add_pawn1_w, add_pawn2_w, add_pawn3_w, add_pawn4_w, add_pawn5_w, add_pawn6_w, add_pawn7_w, add_pawn8_w]
	
	
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
	if timers:
		white_watch = stopwatch("w", font, max_time)
		black_watch = stopwatch("b", font, max_time)
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
	turn_txt = "Ruch białych"
	turn_pawns = white_pawns
	en = []
	check_txt = ""
	adding = False
	check_add=[]
	figure=0

	deciding = True
	first_frame = True
	if timers:
		black_watch.pause_timer()
	print(board.pawns_matrix, ":)")
	backup_tr_w=0
	backup_tr_b=0
	backup_white=white_pawns.copy()
	backup_black=black_pawns.copy()
	backup_white_pos=copy.deepcopy([pw.pos for pw in white_pawns])
	backup_black_pos=copy.deepcopy([pw.pos for pw in black_pawns])
	backup_board=copy.deepcopy(board.pawns_matrix)
	backup_white_add=white_add_buttons.copy()
	backup_black_add=black_add_buttons.copy()
	backup_w_destroyed=copy.deepcopy(w_destroyed)
	backup_b_destroyed=copy.deepcopy(b_destroyed)
	backup_count_w=count_w.copy()
	backup_count_b=count_b.copy()
	backup_white_opp=white_opp.copy()
	backup_black_opp=black_opp.copy()
	back_button=inactive_button((board.res[0]+10+board.pos[0], res[1]/10 *7), [res[0]/12, res[1]/12], (205, 202, 203), "Cofnij")
	ending=False
	repeating_figures_w=[]
	repeating_pos_w=[]
	repeating_reserve_w=[]
	repeating_figures_b=[]
	repeating_pos_b=[]
	repeating_reserve_b=[]
	repeating_figures_w.append([x.type for x in white_pawns])
	repeating_pos_w.append([x.pos for x in white_pawns])
	repeating_reserve_w.append([x.figure for x in white_add_buttons])
	repeating_figures_b.append([x.type for x in black_pawns])
	repeating_pos_b.append([x.pos for x in black_pawns])
	repeating_reserve_b.append([x.figure for x in black_add_buttons])
	backup_rep_fig_w=repeating_figures_w.copy()
	backup_rep_pos_w=repeating_pos_w.copy()
	backup_rep_res_w=repeating_reserve_w.copy()
	backup_rep_fig_b=repeating_figures_b.copy()
	backup_rep_pos_b=repeating_pos_b.copy()
	backup_rep_res_b=repeating_reserve_b.copy()
	repeated=False
	y_8=[font.render("8", True, (0, 0, 0)), (0, int(board.res[1]/16*1+board.pos[1]))]
	y_7=[font.render("7", True, (0, 0, 0)), (0, int(board.res[1]/16*3+board.pos[1]))]
	y_6=[font.render("6", True, (0, 0, 0)), (0, int(board.res[1]/16*5+board.pos[1]))]
	y_5=[font.render("5", True, (0, 0, 0)), (0, int(board.res[1]/16*7+board.pos[1]))]
	y_4=[font.render("4", True, (0, 0, 0)), (0, int(board.res[1]/16*9+board.pos[1]))]
	y_3=[font.render("3", True, (0, 0, 0)), (0, int(board.res[1]/16*11+board.pos[1]))]
	y_2=[font.render("2", True, (0, 0, 0)), (0, int(board.res[1]/16*13+board.pos[1]))]
	y_1=[font.render("1", True, (0, 0, 0)), (0, int(board.res[1]/16*15+board.pos[1]))]
	x_a=[font.render("a", True, (0, 0, 0)), (int(board.res[1]/16*1+board.pos[0]), board.res[1]+board.pos[1])]
	x_b=[font.render("b", True, (0, 0, 0)), (int(board.res[1]/16*3+board.pos[0]), board.res[1]+board.pos[1])]
	x_c=[font.render("c", True, (0, 0, 0)), (int(board.res[1]/16*5+board.pos[0]), board.res[1]+board.pos[1])]
	x_d=[font.render("d", True, (0, 0, 0)), (int(board.res[1]/16*7+board.pos[0]), board.res[1]+board.pos[1])]
	x_e=[font.render("e", True, (0, 0, 0)), (int(board.res[1]/16*9+board.pos[0]), board.res[1]+board.pos[1])]
	x_f=[font.render("f", True, (0, 0, 0)), (int(board.res[1]/16*11+board.pos[0]), board.res[1]+board.pos[1])]
	x_g=[font.render("g", True, (0, 0, 0)), (int(board.res[1]/16*13+board.pos[0]), board.res[1]+board.pos[1])]
	x_h=[font.render("h", True, (0, 0, 0)), (int(board.res[1]/16*15+board.pos[0]), board.res[1]+board.pos[1])]
	cords=[y_8, y_7, y_6, y_5, y_4, y_3, y_2, y_1, x_a, x_b, x_c, x_d, x_e, x_f, x_g ,x_h]
	white_reserve=[]
	black_reserve=[]
	white_reserve_backup=[]
	black_reserve_backup=[]
	
	while playing:
		while transform: #Kiedy pionek zmieniany jest na inną figurę
			transform_w.draw(game_window)
			if tr.color=="w":
				rook_w_button.undertext="Wieża("+str(w_destroyed["rook"])+")"
				rook_w_button.draw(game_window)
				knight_w_button.undertext="Skoczek("+str(w_destroyed["knight"])+")"
				knight_w_button.draw(game_window)
				bishop_w_button.undertext="Goniec("+str(w_destroyed["bishop"])+")"
				bishop_w_button.draw(game_window)
				queen_w_button.undertext="Hetman("+str(w_destroyed["queen"])+")"
				queen_w_button.draw(game_window)
			else:
				rook_b_button.undertext="Wieża("+str(b_destroyed["rook"])+")"
				rook_b_button.draw(game_window)
				knight_b_button.undertext="Skoczek("+str(b_destroyed["knight"])+")"
				knight_b_button.draw(game_window)
				bishop_b_button.undertext="Goniec("+str(b_destroyed["bishop"])+")"
				bishop_b_button.draw(game_window)
				queen_b_button.undertext="Hetman("+str(b_destroyed["queen"])+")"
				queen_b_button.draw(game_window)
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key==27:
						playing=False
						deciding=False
						running=False
						transform==False
				if event.type == pygame.QUIT:
					playing=False
					deciding=False
					running=False
					transform==False
				elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					if tr.color=="w":
						white_reserve_backup=[rv.copy() for rv in white_reserve]
						backup_figures_w=[fig.type for fig in white_pawns]
						if rook_w_button.rect.collidepoint(event.pos) and w_destroyed["rook"]>0:
							w_destroyed["rook"]-=1
							tr.transform("rook", rook_w_png)
							for rsv in white_reserve:
								if rsv[0].figure=="rook" and rsv[1]==1:
									rsv[1]=0
									break
							transform=False
						elif knight_w_button.rect.collidepoint(event.pos) and w_destroyed["knight"]>0:
							w_destroyed["knight"]-=1
							tr.transform("knight", knight_w_png)
							for rsv in white_reserve:
								if rsv[0].figure=="knight" and rsv[1]==1:
									rsv[1]=0
									break
							transform=False
						elif bishop_w_button.rect.collidepoint(event.pos) and w_destroyed["bishop"]>0:
							w_destroyed["bishop"]-=1
							tr.transform("bishop", bishop_w_png)
							for rsv in white_reserve:
								if rsv[0].figure=="bishop" and rsv[1]==1:
									rsv[1]=0
									break
							transform=False
						elif queen_w_button.rect.collidepoint(event.pos) and w_destroyed["queen"]>0:
							w_destroyed["queen"]-=1
							tr.transform("queen", queen_w_png)
							for rsv in white_reserve:
								if rsv[0].figure=="queen" and rsv[1]==1:
									rsv[1]=0
									break
							transform=False
					else:
						black_reserve_backup=[rv.copy() for rv in black_reserve]
						#black_reserve_backup=[[bck[0].type, bck[1]] for bck in black_reserve]
						backup_figures_b=[fig.type for fig in black_pawns]
						if rook_b_button.rect.collidepoint(event.pos) and b_destroyed["rook"]>0:
							b_destroyed["rook"]-=1
							tr.transform("rook", rook_b_png)
							for rsv in black_reserve:
								if rsv[0].figure=="rook" and rsv[1]==1:
									rsv[1]=0
									break
							transform=False
						elif knight_b_button.rect.collidepoint(event.pos) and b_destroyed["knight"]>0:
							b_destroyed["knight"]-=1
							tr.transform("knight", knight_b_png)
							for rsv in black_reserve:
								if rsv[0].figure=="knight" and rsv[1]==1:
									rsv[1]=0
									break
							transform=False
						elif bishop_b_button.rect.collidepoint(event.pos) and b_destroyed["bishop"]>0:
							b_destroyed["bishop"]-=1
							tr.transform("bishop", bishop_b_png)
							for rsv in black_reserve:
								if rsv[0].figure=="bishop" and rsv[1]==1:
									rsv[1]=0
									break
							transform=False
						elif queen_b_button.rect.collidepoint(event.pos) and b_destroyed["queen"]>0:
							b_destroyed["queen"]-=1
							tr.transform("queen", queen_b_png)
							for rsv in black_reserve:
								if rsv[0].figure=="queen" and rsv[1]==1:
									rsv[1]=0
									break
							transform=False
			if transform==False:
				en=is_check(turn, white_pawns, black_pawns, board, game_window, w_destroyed, b_destroyed)
				if en!=[]: #blokowanie ruchow gdy jest szach
					#aktualizacja pozycji na pawn_matrix aby poprawnie sprwadzić możliwe ruchy przy szachu
					for white_pawn in white_pawns:
						white_pawn.draw(game_window, board)
					for black_pawn in black_pawns:
						black_pawn.draw(game_window, board)
					check_txt=is_mat(en, turn, white_pawns, black_pawns, board, game_window, w_destroyed, b_destroyed)
				if tr.color=="w":
					backup_tr_w=1
					repeating_figures_w=[]
					repeating_pos_w=[]
					repeating_reserve_w=[]
					repeating_figures_w.append([x.type for x in white_pawns])
					repeating_pos_w.append([x.pos for x in white_pawns])
					repeating_reserve_w.append([x.figure for x in white_add_buttons])
				else:
					backup_tr_b=1
					repeating_figures_b=[]
					repeating_pos_b=[]
					repeating_reserve_b=[]
					repeating_figures_b.append([x.type for x in black_pawns])
					repeating_pos_b.append([x.pos for x in black_pawns])
					repeating_reserve_b.append([x.figure for x in black_add_buttons])
			pygame.display.update()
		while adding:  # Dodawanie figury na szachownice		
			if add_first_frame:
				if turn == "white":
					if add_fig_but.figure=="rook":
						temp=pawn(rook_w_png, (-1,-1), pawn_res, "rook", "w")
					elif add_fig_but.figure=="knight":
						temp=pawn(knight_w_png, (-1,-1), pawn_res, "knight", "w")
					elif add_fig_but.figure=="bishop":
						temp=pawn(bishop_w_png, (-1,-1), pawn_res, "bishop", "w")
					elif add_fig_but.figure=="queen":
						temp=pawn(queen_w_png, (-1,-1), pawn_res, "queen", "w")
					elif add_fig_but.figure=="pawn":
						temp=pawn(pawn_w_png, (-1,-1), pawn_res, "pawn", "w")
					elif add_fig_but.figure=="king":
						temp=pawn(king_w_png, (-1,-1), pawn_res, "king", "w")
				else:
					if add_fig_but.figure=="rook":
						temp=pawn(rook_b_png, (-1,-1), pawn_res, "rook", "b")
					elif add_fig_but.figure=="knight":
						temp=pawn(knight_b_png, (-1,-1), pawn_res, "knight", "b")
					elif add_fig_but.figure=="bishop":
						temp=pawn(bishop_b_png, (-1,-1), pawn_res, "bishop", "b")
					elif add_fig_but.figure=="queen":
						temp=pawn(queen_b_png, (-1,-1), pawn_res, "queen", "b")
					elif add_fig_but.figure=="pawn":
						temp=pawn(pawn_b_png, (-1,-1), pawn_res, "pawn", "b")
					elif add_fig_but.figure=="king":
						temp=pawn(king_b_png, (-1,-1), pawn_res, "king", "b")
				possible_pos=board.add_positions(white_pawns, black_pawns, turn, temp, w_destroyed, b_destroyed, game_window)
				position_rects=[move_rect(x, board.area) for x in possible_pos]
				if check_txt!="":
					possible_pos=check_add
					position_rects=[move_rect(x, board.area) for x in possible_pos]
				add_first_frame=0
			''' jakas pozostalosc po straej funkcji, zobaczymy czy potrzebna dalej
			if not add_w.rect.collidepoint(event.pos) and temp==0:
				adding=0
				check_add=[]
			'''
			#Postawienie wybranej figury na szachownicty
			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key==27:
						playing = False
						deciding = False
						running = False
						adding == False
				if event.type == pygame.QUIT:
					playing = False
					deciding = False
					running = False
					adding == False
				if event.type == pygame.MOUSEBUTTONUP:
					mouse_pos = pygame.mouse.get_pos()
					x=-1
					y=-1
					i=0
					for area in board.pos_areas():
						if area[0]+board.pos[0] < mouse_pos[0] and area[1]+board.pos[0] > mouse_pos[0]:
							x = i
						if area[0]+board.pos[1] < mouse_pos[1] and area[1]+board.pos[1] > mouse_pos[1]:
							y = i
						i += 1
					if x!=-1 and y!=-1 and [x,y] in possible_pos:
						backup_tr_w=0
						backup_tr_b=0
						backup_white=white_pawns.copy()
						backup_black=black_pawns.copy()
						backup_white_pos=copy.deepcopy([pw.pos for pw in white_pawns])
						backup_black_pos=copy.deepcopy([pw.pos for pw in black_pawns])
						backup_board=copy.deepcopy(board.pawns_matrix)
						backup_white_add=white_add_buttons.copy()
						backup_black_add=black_add_buttons.copy()
						backup_w_destroyed=copy.deepcopy(w_destroyed)
						backup_b_destroyed=copy.deepcopy(b_destroyed)
						backup_count_w=count_w.copy()
						backup_count_b=count_b.copy()
						backup_white_opp=white_opp.copy()
						backup_black_opp=black_opp.copy()
						white_reserve_backup=[rv.copy() for rv in white_reserve]
						black_reserve_backup=[rv.copy() for rv in black_reserve]
						back_button.status=1
						board.append_figure(temp, (x,y), white_pawns, black_pawns)
						adding=0
						if temp.color=="w":
							count_w[temp.type]-=1
							del(white_add_buttons[white_add_buttons.index(add_fig_but)])
							backup_rep_fig_w=repeating_figures_w.copy()
							backup_rep_pos_w=repeating_pos_w.copy()
							backup_rep_res_w=repeating_reserve_w.copy()
							repeating_figures_w=[]
							repeating_pos_w=[]
							repeating_reserve_w=[]
							repeating_figures_w.append([x.type for x in white_pawns])
							repeating_pos_w.append([x.pos for x in white_pawns])
							repeating_reserve_w.append([x.figure for x in white_add_buttons])
						else:
							count_b[temp.type]-=1
							del(black_add_buttons[black_add_buttons.index(add_fig_but)])

							backup_rep_fig_b=repeating_figures_b.copy()
							backup_rep_pos_b=repeating_pos_b.copy()
							backup_rep_res_b=repeating_reserve_b.copy()
							repeating_figures_b=[]
							repeating_pos_b=[]
							repeating_reserve_b=[]
							repeating_figures_b.append([x.type for x in black_pawns])
							repeating_pos_b.append([x.pos for x in black_pawns])
							repeating_reserve_b.append([x.figure for x in black_add_buttons])
						en=[]
						check_add=[]
						if turn == "white":
							turn = "black"
							turn_pawns = black_pawns
							turn_txt = "Ruch czarnych"
							for i in range(len(white_opp)):
								if white_opp[i].figure==temp.type:
									if white_opp[i].figure not in ["king", "pawn"]:
										white_reserve.append([white_opp.pop(white_opp.index(white_opp[i])), 0])
										white_reserve[-1][0].pos=(board.res[0]+board.pos[0]+mini_pawn_res[0]*len(white_reserve)-mini_pawn_res[0],res[1]/10*3)
										print([x[0].figure for x in white_reserve])
									else:
										del(white_opp[i])
									break
							if timers:
								black_watch.resume()
								white_watch.pause_timer()
						else:
							turn = "white"
							turn_pawns = white_pawns
							turn_txt = "Ruch białych"
							for i in range(len(black_opp)):
								if black_opp[i].figure==temp.type:
									if black_opp[i].figure not in ["king", "pawn"]:
										black_reserve.append([black_opp.pop(black_opp.index(black_opp[i])), 0])
										black_reserve[-1][0].pos=(board.res[0]+board.pos[0]+mini_pawn_res[0]*len(black_reserve)-mini_pawn_res[0],res[1]/10*3)
										print([x[0].figure for x in black_reserve])
									else:
										del(black_opp[i])
									break
							if timers:
								white_watch.resume()
								black_watch.pause_timer()
						check_txt=""
					else:
						adding=0
						temp=0
						add_fig_but=0
					figure=0
					temp=0
				game_window.fill(bg_color)
				board.draw(game_window)
				for white_pawn in white_pawns:
					white_pawn.draw(game_window, board)
				for black_pawn in black_pawns:
					black_pawn.draw(game_window, board)
				if timers:
					white_watch.update(game_window, board)
					black_watch.update(game_window, board)
				for x in position_rects:
					x.draw_moves(game_window, board)
				if temp!=0:
					mouse_pos = pygame.mouse.get_pos()
					temp.mouse_dragging(game_window, mouse_pos, pawn_res)
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
		if timers:
			if black_watch.remaining_time == 0 or white_watch.remaining_time == 0 or check_txt == "Szach-Mat!" or (w_destroyed["king"]==1 or b_destroyed["king"]==1):
				ending=1
				if black_watch.remaining_time==0:
					turn_txt="Wygrały czarne"
				elif white_watch.remaining_time==0:
					turn_txt="Wygrały białe"
				elif check_txt == "Szach-Mat!" and turn=="white":
					turn_txt="Wygrały czarne"
				elif check_txt == "Szach-Mat!" and turn=="black":
					turn_txt="Wygrały białe"
				elif w_destroyed["king"]==1:
					turn_txt="Wygrały czarne"
				elif b_destroyed["king"]==1:
					turn_txt="Wygrały białe"
				playing=False
		else:
			if check_txt == "Szach-Mat!" or (w_destroyed["king"]==1 or b_destroyed["king"]==1):
				ending=1
				if check_txt == "Szach-Mat!" and turn=="white":
					turn_txt="Wygrały czarne"
				elif check_txt == "Szach-Mat!" and turn=="black":
					turn_txt="Wygrały białe"
				elif w_destroyed["king"]==1:
					turn_txt="Wygrały czarne"
				elif b_destroyed["king"]==1:
					turn_txt="Wygrały białe"
				playing = False
		if repeated==True:
			turn_txt="Remis, potrójne powtórzenie"
			ending=True
			playing=False
		pygame.time.Clock().tick(30)
		game_window.fill(bg_color)
		board.draw(game_window)
		game_window.blit(font.render(turn_txt, True, (0, 0, 0)), (board.res[0]+15+board.pos[0], 15))
		game_window.blit(font.render(check_txt, True, (0, 0, 0)), (board.res[0]+15+board.pos[0], board.res[1]/2+board.pos[1]))
		if timers:
			white_watch.update(game_window, board)
			black_watch.update(game_window, board)

		for white_pawn in white_pawns:
			white_pawn.draw(game_window, board)
		for black_pawn in black_pawns:
			black_pawn.draw(game_window, board)
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key==27:
					playing = False
					deciding = False
					running = False
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
				if turn=="white":
					if "king" in [b.figure for b in white_add_buttons]:
						for x in white_add_buttons:
							if x.figure=="king":
								if x.rect.collidepoint(event.pos):
									add_fig_but=x
									adding=1
									add_first_frame=1
									if en!=[]:
										check_add=add_defence(count_w, count_b, board, turn, en, turn_pawns, game_window, white_pawns, black_pawns, w_destroyed, b_destroyed)
										if check_txt=="Szach_Mat!" and check_add!=[]:
											check_txt=""
									break
					else:
						for x in white_add_buttons:
							if x.rect.collidepoint(event.pos):
								add_fig_but=x
								adding=1
								add_first_frame=1
								if en!=[]:
									check_add=add_defence(count_w, count_b, board, turn, en, turn_pawns, game_window, white_pawns, black_pawns, w_destroyed, b_destroyed)
									if check_txt=="Szach_Mat!" and check_add!=[]:
										check_txt=""
								break
				else:
					if "king" in [b.figure for b in black_add_buttons]:
						for x in black_add_buttons:
							if x.figure=="king":
								if x.rect.collidepoint(event.pos):
									add_fig_but=x
									adding=1
									add_first_frame=1
									if en!=[]:
										check_add=add_defence(count_w, count_b, board, turn, en, turn_pawns, game_window, white_pawns, black_pawns, w_destroyed, b_destroyed)
										if check_txt=="Szach_Mat!" and check_add!=[]:
											check_txt=""
									break
					else:
						for x in black_add_buttons:
							if x.rect.collidepoint(event.pos):
								add_fig_but=x
								adding=1
								add_first_frame=1
								if en!=[]:
									check_add=add_defence(count_w, count_b, board, turn, en, turn_pawns, game_window, white_pawns, black_pawns, w_destroyed, b_destroyed)
									if check_txt=="Szach_Mat!" and check_add!=[]:
										check_txt=""
								break
				if back_button.rect.collidepoint(event.pos) and back_button.status==1:
					back_button.status=0
					white_pawns=backup_white
					black_pawns=backup_black
					for i in range(len(backup_white_pos)):
						white_pawns[i].pos=backup_white_pos[i]
					for i in range(len(backup_black_pos)):
						black_pawns[i].pos=backup_black_pos[i]
					if backup_tr_w:
						for i in range(len(white_pawns)):
							if white_pawns[i].type!=backup_figures_w[i]:
								white_pawns[i].transform("pawn", pawn_w_png)
								backup_tr_w=0
								break
					if backup_tr_b:
						for i in range(len(black_pawns)):
							if black_pawns[i].type!=backup_figures_b[i]:
								black_pawns[i].transform("pawn", pawn_b_png)
								backup_tr_b=0
								break
					white_reserve=white_reserve_backup
					black_reserve=black_reserve_backup
					board.pawns_matrix=backup_board
					white_add_buttons=backup_white_add
					black_add_buttons=backup_black_add
					w_destroyed=backup_w_destroyed
					b_destroyed=backup_b_destroyed
					count_w=backup_count_w
					count_b=backup_count_b
					white_opp=backup_white_opp
					black_opp=backup_black_opp
					repeating_figures_w=backup_rep_fig_w
					repeating_pos_w=backup_rep_pos_w
					repeating_reserve_w=backup_rep_res_w
					repeating_figures_b=backup_rep_fig_b
					repeating_pos_b=backup_rep_pos_b
					repeating_reserve_b=backup_rep_res_b
					print(repeating_figures_w, repeating_pos_w)
					if turn == "white":
						turn = "black"
						turn_pawns = black_pawns
						turn_txt = "Ruch czarnych"
						if timers:
							black_watch.resume()
							white_watch.pause_timer()
					else:
						turn = "white"
						turn_pawns = white_pawns
						turn_txt = "Ruch białych"
						if timers:
							white_watch.resume()
							black_watch.pause_timer()
					en = is_check(turn, white_pawns, black_pawns, board, game_window, w_destroyed, b_destroyed)
					if en != []:  # blokowanie ruchow gdy jest szach
						# aktualizacja pozycji na pawn_matrix aby poprawnie sprwadzić możliwe ruchy przy szachu
						for white_pawn in white_pawns:
							white_pawn.draw(game_window, board)
						for black_pawn in black_pawns:
							black_pawn.draw(game_window, board)
						check_txt=is_mat(en, turn, white_pawns, black_pawns, board, game_window, w_destroyed, b_destroyed)
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
						backup_tr_w=0
						backup_tr_b=0
						backup_white=white_pawns.copy()
						backup_black=black_pawns.copy()
						backup_white_pos=copy.deepcopy([pw.pos for pw in white_pawns])
						backup_black_pos=copy.deepcopy([pw.pos for pw in black_pawns])
						backup_board=copy.deepcopy(board.pawns_matrix)
						backup_white_add=white_add_buttons.copy()
						backup_black_add=black_add_buttons.copy()
						backup_w_destroyed=copy.deepcopy(w_destroyed)
						backup_b_destroyed=copy.deepcopy(b_destroyed)
						backup_count_w=count_w.copy()
						backup_count_b=count_b.copy()
						backup_white_opp=white_opp.copy()
						backup_black_opp=black_opp.copy()
						white_reserve_backup=[rv.copy() for rv in white_reserve]
						black_reserve_backup=[rv.copy() for rv in black_reserve]
						back_button.status=1
						hw.pos = (x, y)
						if turn=="black":
							for op in white_pawns:
								if op.pos==(x,y):
									for rsv in white_reserve:
										if rsv[0].figure==op.type and rsv[1]==0:
											rsv[1]=1
											break										
									break
						else:
							for op in black_pawns:
								if op.pos==(x,y):
									for rsv in black_reserve:
										if rsv[0].figure==op.type and rsv[1]==0:
											rsv[1]=1
											print(black_reserve)
											print(black_reserve_backup)
											break										
									break
						destroy_enemy((x, y), turn, white_pawns, black_pawns, w_destroyed, b_destroyed)
						check = False
						if turn == "white":
							backup_rep_fig_w=repeating_figures_w.copy()
							backup_rep_pos_w=repeating_pos_w.copy()
							backup_rep_res_w=repeating_reserve_w.copy()
							repeating_figures_w=[]
							repeating_pos_w=[]
							repeating_reserve_w=[]
							repeating_figures_w.append([x.type for x in white_pawns])
							repeating_pos_w.append([x.pos for x in white_pawns])
							repeating_reserve_w.append([x.figure for x in white_add_buttons])
							turn = "black"
							turn_pawns = black_pawns
							turn_txt = "Ruch czarnych"
							if timers:
								black_watch.resume()
								white_watch.pause_timer()
						else:
							backup_rep_fig_b=repeating_figures_b.copy()
							backup_rep_pos_b=repeating_pos_b.copy()
							backup_rep_res_b=repeating_reserve_b.copy()
							repeating_figures_b=[]
							repeating_pos_b=[]
							repeating_reserve_b=[]
							repeating_figures_b.append([x.type for x in black_pawns])
							repeating_pos_b.append([x.pos for x in black_pawns])
							repeating_reserve_b.append([x.figure for x in black_add_buttons])
							turn = "white"
							turn_pawns = white_pawns
							turn_txt = "Ruch białych"
							if timers:
								white_watch.resume()
								black_watch.pause_timer()
						check_txt = ""
						if hw.type == "pawn" and ((hw.color == "w" and hw.pos[1] == 0) or (hw.color == "b" and hw.pos[1] == 7)):
							transform = True
							tr = hw
							backup_white=white_pawns.copy()
							backup_black=black_pawns.copy()
							backup_white_pos=copy.deepcopy([pw.pos for pw in white_pawns])
							backup_black_pos=copy.deepcopy([pw.pos for pw in black_pawns])
							backup_board=copy.deepcopy(board.pawns_matrix)
							backup_white_add=white_add_buttons.copy()
							backup_black_add=black_add_buttons.copy()
							backup_w_destroyed=copy.deepcopy(w_destroyed)
							backup_b_destroyed=copy.deepcopy(b_destroyed)
							backup_count_w=count_w.copy()
							backup_count_b=count_b.copy()
							backup_white_opp=white_opp.copy()
							backup_black_opp=black_opp.copy()
							back_button.status=1				
						if transform == False:
							en = is_check(turn, white_pawns, black_pawns, board, game_window, w_destroyed, b_destroyed)
							if en != []:  # blokowanie ruchow gdy jest szach
								# aktualizacja pozycji na pawn_matrix aby poprawnie sprwadzić możliwe ruchy przy szachu
								for white_pawn in white_pawns:
									white_pawn.draw(game_window, board)
								for black_pawn in black_pawns:
									black_pawn.draw(game_window, board)
								check_txt=is_mat(en, turn, white_pawns, black_pawns, board, game_window, w_destroyed, b_destroyed)
					elif [x, y] in hw.mv:
						print(board.pawns_matrix, ":)")
						backup_tr_w=0
						backup_tr_b=0
						backup_white=white_pawns.copy()
						backup_black=black_pawns.copy()
						backup_white_pos=copy.deepcopy([pw.pos for pw in white_pawns])
						backup_black_pos=copy.deepcopy([pw.pos for pw in black_pawns])
						backup_board=copy.deepcopy(board.pawns_matrix)
						backup_white_add=white_add_buttons.copy()
						backup_black_add=black_add_buttons.copy()
						backup_w_destroyed=copy.deepcopy(w_destroyed)
						backup_b_destroyed=copy.deepcopy(b_destroyed)
						backup_count_w=count_w.copy()
						backup_count_b=count_b.copy()
						backup_white_opp=white_opp.copy()
						backup_black_opp=black_opp.copy()
						back_button.status=1
						hw.pos = (x, y)
						check = False
						if turn == "white":
							turn = "black"
							turn_pawns = black_pawns
							turn_txt = "Ruch czarnych"
							backup_rep_fig_w=repeating_figures_w.copy()
							backup_rep_pos_w=repeating_pos_w.copy()
							backup_rep_res_w=repeating_reserve_w.copy()
							figs=[x.type for x in white_pawns]
							poses=[x.pos for x in white_pawns]
							resv=[x.figure for x in white_add_buttons]
							if poses in repeating_pos_w:
								ind=repeating_pos_w.index(poses)
								if figs==repeating_figures_w[ind] and resv==repeating_reserve_w[ind]:
									rep=0
									for i in range(len(repeating_pos_w)):
										if repeating_pos_w[i]==poses and repeating_figures_w[i]==figs and repeating_reserve_w[i]==resv:
											rep+=1
											if rep==2:
												repeated=True
												break
										
							repeating_pos_w.append(poses)
							repeating_figures_w.append(figs)
							repeating_reserve_w.append(resv)
							
							if timers:
								black_watch.resume()
								white_watch.pause_timer()
						else:
							turn = "white"
							turn_pawns = white_pawns
							turn_txt = "Ruch białych"
							figs=[x.type for x in black_pawns]
							poses=[x.pos for x in black_pawns]
							resv=[x.figure for x in black_add_buttons]
							backup_rep_fig_b=repeating_figures_b.copy()
							backup_rep_pos_b=repeating_pos_b.copy()
							backup_rep_res_b=repeating_reserve_b.copy()
							if poses in repeating_pos_b:
								ind=repeating_pos_b.index(poses)
								if figs==repeating_figures_b[ind] and resv==repeating_reserve_b[ind]:
									rep=0
									for i in range(len(repeating_pos_b)):
										if repeating_pos_b[i]==poses and repeating_figures_b[i]==figs and repeating_reserve_b[i]==resv:
											rep+=1
											if rep==2:
												repeated=True
												break
							repeating_figures_b.append(figs)
							repeating_pos_b.append(poses)
							repeating_reserve_b.append(resv)
							if timers:
								white_watch.resume()
								black_watch.pause_timer()
						check_txt = ""
						if hw.type == "pawn" and ((hw.color == "w" and hw.pos[1] == 0) or (hw.color == "b" and hw.pos[1] == 7)):
							transform = True
							tr = hw
						if transform == False:
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
			hw.mouse_dragging(game_window, mouse_pos, pawn_res)
		first_frame = False
		
		for x in cords:
			game_window.blit(x[0],x[1])
		if turn=="white":
			if "king" in [x.figure for x in white_add_buttons]:
				for but in white_add_buttons:
					if but.figure=="king":
						but.draw(game_window)
						break
			else:
				for but in white_add_buttons:
					but.draw(game_window)
			for x in white_reserve:
				if "pawn" in [p.type for p in white_pawns] or "pawn" in [p.figure for p in white_add_buttons]:
					if x[1]==1:
						x[0].draw(game_window)
		else:
			if "king" in [x.figure for x in black_add_buttons]:
				for but in black_add_buttons:
					if but.figure=="king":
						but.draw(game_window)
						break
			else:
				for but in black_add_buttons:
					but.draw(game_window)
			for x in black_reserve:
				if "pawn" in [p.type for p in black_pawns] or "pawn" in [p.figure for p in black_add_buttons]:
					if x[1]==1:
						x[0].draw(game_window)		
		back_button.draw(game_window)
		if turn=="white":
			for opp in black_opp:
				opp.draw(game_window)
		else:
			for opp in white_opp:
				opp.draw(game_window)
		pygame.display.update()
	'''
	while deciding:
		end_game_w.draw(game_window)
		again_button.draw(game_window)
		quit_button.draw(game_window)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				deciding = False
				running = False
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if again_button.rect.collidepoint(event.pos):
					deciding = False
				if quit_button.rect.collidepoint(event.pos):
					deciding = False
					running = False
		pygame.display.update()
	'''
	while ending:
		pygame.time.Clock().tick(30)
		game_window.fill(bg_color)
		board.draw(game_window)
		game_window.blit(font.render(turn_txt, True, (0, 0, 0)), (board.res[0]+15+board.pos[0], 15))
		game_window.blit(font.render(check_txt, True, (0, 0, 0)), (board.res[0]+15+board.pos[0], board.res[1]/2+board.pos[1]))
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key==27:
					ending=False
			if event.type == pygame.QUIT:
				ending=False
		if turn=="white":
			if "king" in [x.figure for x in white_add_buttons]:
				for but in white_add_buttons:
					if but.figure=="king":
						but.draw(game_window)
						break
			else:
				for but in white_add_buttons:
					but.draw(game_window)
		else:
			if "king" in [x.figure for x in black_add_buttons]:
				for but in black_add_buttons:
					if but.figure=="king":
						but.draw(game_window)
						break
			else:
				for but in black_add_buttons:
					but.draw(game_window)
		
		back_button.draw(game_window)
		for x in cords:
			game_window.blit(x[0], x[1])
		if turn=="white":
			for opp in black_opp:
				opp.draw(game_window)
		else:
			for opp in white_opp:
				opp.draw(game_window)
		for white_pawn in white_pawns:
			white_pawn.draw(game_window, board)
		for black_pawn in black_pawns:
			black_pawn.draw(game_window, board)
		pygame.display.update()
#kings_chess(game_window, res)


