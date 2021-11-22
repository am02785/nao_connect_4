# The Connect4 class which represents the connect4 game
from logging import exception

from grid import Grid


class Connect4:

    # The constructor of the Connect4 class
    def __init__(self):
        # The player attribute which specifies who's turn it is
        self.__player = 'player 1'
        # The grid attribute which represents the grid in the game
        self.__grid = Grid()
        # The player_1_colour attribute which represents the colour
        # of the counter player 1 uses
        self.__player_1_colour = ''
        # The player_2_colour attribute which represents the colour
        # of the counter player 2 uses
        self.__player_2_colour = ''
        # starts the game
        self.__play_game()

