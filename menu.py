import pygame
import pygame_menu
from pygame_menu import themes
from kings_chess import *
from online_lobby import *
from kings_chess_online import *

def play_local():
	global game_window, res
	kings_chess(game_window, res)
	
def play_online():
	global game_window, res
	online_menu(game_window, res, "Simek")
	



pygame.init()
res=(800,600)
game_window = pygame.display.set_mode(res)
pygame.display.set_caption("Szachy Królewskie")

mainmenu = pygame_menu.Menu('Szachy królewskie', res[0], res[1], theme=themes.THEME_BLUE)
mainmenu.add.text_input('Nick: ', default='Nick', maxchar=20)
mainmenu.add.button('Gra na jednym komputerze', play_local)
mainmenu.add.button('Gra sieciowa', play_online)
mainmenu.add.button('Wyjście', pygame_menu.events.EXIT)
 
#level = pygame_menu.Menu('Select a Difficulty', 600, 400, theme=themes.THEME_BLUE)
#level.add.selector('Difficulty:',[('Hard',1),('Easy',2)], onchange=set_difficulty)

mainmenu.mainloop(game_window)