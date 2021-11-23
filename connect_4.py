# The Connect4 class which represents the connect4 game
from random import randint
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

    # Plays the connect4 game
    def __play_game(self):
        # Asks player 1 to choose the colour of the counter
        self.__player_1_colour = raw_input("Enter which colour you want to use:")
        if self.__player_1_colour == 'r':
            self.__player_2_colour = 'y'
        elif self.__player_1_colour == 'y':
            self.__player_2_colour = 'r'
        else:
            raise Exception()
        print('\n')

        while True:
            print(self.__grid.__str__() + '\n')
            print(self.__player + '\'s turn\n')

            if self.__player == 'player 1':
                hole_number = int(raw_input("Which hole number do you want to put the counter in:"))
                print('\n')
                self.__grid.add_counter_to_grid(self.__player_1_colour, hole_number)
                if self.__grid.check_if_game_won(self.__player_1_colour):
                    break
                else:
                    self.__player = 'player 2'

            elif self.__player == 'player 2':
                hole_number = int(raw_input("Which hole number do you want to put the counter in:"))
                print('\n')
                self.__grid.add_counter_to_grid(self.__player_2_colour, hole_number)
                if self.__grid.check_if_game_won(self.__player_2_colour):
                    break
                else:
                    self.__player = 'player 1'

        print(self.__grid.__str__() + '\n')
        print(self.__player + ' won')
        print('\n')

if __name__ == '__main__':
    Connect4()
