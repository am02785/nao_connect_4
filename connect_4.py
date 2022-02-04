# The Connect4 class which represents the connect4 game
import cv2
import naoqi
import numpy as np
import random
import nao_motion_controller
import nao_video_controller

ip_address = "127.0.0.1"
port = 9559
tts = naoqi.ALProxy("ALTextToSpeech", ip_address, port)

class Connect4:

    # The constructor of the Connect4 class
    def __init__(self):
        # The player attribute which specifies who's turn it is
        self.__player = 'player 1'
        # The grid attribute which represents the grid in the game
        self.__grid = [['*' for y in range(6)] for x in range(7)]
        # The player_1_colour attribute which represents the colour
        # of the counter player 1 uses
        self.__player_1_colour = ''
        # The player_2_colour attribute which represents the colour
        # of the counter player 2 uses
        self.__player_2_colour = ''
        # The number_of_turns attribute which represents the number
        # of turns left
        self.__number_of_turns = 42
        # starts the game
        self.__play_game()


    # Adds a counter to the grid based on the colour of the counter
    # and upper hole number
    def add_counter_to_grid(self, colour, grid, hole_number):
        for x in range(len(grid[hole_number])):
            if grid[hole_number][x] == '*':
                grid[hole_number][x] = colour
                break


    # Checks if a player has won the game based on the colour of the counter
    # used https://stackoverflow.com/questions/29949169/python-connect-4-check-win-function
    def check_if_game_won(self, colour, grid):
        # Checks the horizontal spaces
        for y in range(len(grid[0])):
            for x in range(len(grid) - 3):
                if grid[x][y] == colour and grid[x+1][y] == colour and grid[x+2][y] == colour and grid[x+3][y] == colour:
                    return True

        # Checks the vertical spaces
        for x in range(len(grid)):
            for y in range(len(grid[0]) - 3):
                if grid[x][y] == colour and grid[x][y+1] == colour and grid[x][y+2] == colour and grid[x][y+3] == colour:
                    return True

        # Checks the positively sloped diagonal spaces
        for x in range(len(grid) - 3):
            for y in range(len(grid[0]) - 3):
                if grid[x][y] == colour and grid[x+1][y+1] == colour and grid[x+2][y+2] == colour and grid[x+3][y+3] == colour:
                    return True

        # Checks the negatively sloped diagonal spaces
        for x in range(len(grid) - 3):
            for y in range(3, len(grid[0])):
                if grid[x][y] == colour and grid[x+1][y-1] == colour and grid[x+2][y-2] == colour and grid[x+3][y-3] == colour:
                    return True

        return False

    # Returns a score for the board position
    # used https://github.com/kupshah/Connect-Four/blob/master/player.py
    def score_position(self, player_1_colour, player_2_colour, grid):
        score = 0
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                # Checks the horizontal spaces
                try:
                    if grid[x][y] == grid[x+1][y] == player_2_colour:
                        score += 10
                    if grid[x][y] == grid[x+1][y] == grid[x+2][y] == player_2_colour:
                        score += 100
                    if grid[x][y] == grid[x+1][y] == grid[x+2][y] == grid[x+3][y] == player_2_colour:
                        score += 10000

                    if grid[x][y] == grid[x+1][y] == player_1_colour:
                        score -= 10
                    if grid[x][y] == grid[x+1][y] == grid[x+2][y] == player_1_colour:
                        score -= 100
                    if grid[x][y] == grid[x+1][y] == grid[x+2][y] == grid[x+3][y] == player_1_colour:
                        score -= 10000
                except IndexError:
                    pass

                # Checks the vertical spaces
                try:
                    if grid[x][y] == grid[x][y+1] == player_2_colour:
                        score += 10
                    if grid[x][y] == grid[x][y+1] == grid[x][y+2] == player_2_colour:
                        score += 100
                    if grid[x][y] == grid[x][y+1] == grid[x][y+2] == grid[x][y+3] == player_2_colour:
                        score += 10000

                    if grid[x][y] == grid[x][y+1] == player_1_colour:
                        score -= 10
                    if grid[x][y] == grid[x][y+1] == grid[x][y+2] == player_1_colour:
                        score -= 100
                    if grid[x][y] == grid[x][y+1] == grid[x][y+2] == grid[x][y+3] == player_1_colour:
                        score -= 10000
                except IndexError:
                    pass

                # Checks the positively sloped diagonal spaces
                try:
                    if grid[x][y] == grid[x+1][y+1] == player_2_colour:
                        score += 10
                    if grid[x][y] == grid[x+1][y+1] == grid[x+2][y+2] == player_2_colour:
                        score += 100
                    if grid[x][y] == grid[x+1][y+1] == grid[x+2][y+2] == grid[x+3][y+3] == player_2_colour:
                        score += 10000

                    if grid[x][y] == grid[x+1][y+1] == player_1_colour:
                        score -= 10
                    if grid[x][y] == grid[x+1][y+1] == grid[x+2][y+2] == player_1_colour:
                        score -= 100
                    if grid[x][y] == grid[x+1][y+1] == grid[x+2][y+2] == grid[x+3][y+3] == player_1_colour:
                        score -= 10000
                except IndexError:
                    pass

                # Checks the negatively sloped diagonal spaces
                try:
                    if grid[x][y] == grid[x+1][y-1] == player_2_colour:
                        score += 10
                    if grid[x][y] == grid[x+1][y-1] == grid[x+2][y-2] == player_2_colour:
                        score += 100
                    if grid[x][y] == grid[x+1][y] == grid[x+2][y-2] == grid[x+3][y-3] == player_2_colour:
                        score += 10000

                    if grid[x][y] == grid[x+1][y-1] == player_1_colour:
                        score -= 10
                    if grid[x][y] == grid[x+1][y-1] == grid[x+2][y-2] == player_1_colour:
                        score -= 100
                    if grid[x][y] == grid[x+1][y-1] == grid[x+2][y-2] == grid[x+3][y-3] == player_1_colour:
                        score -= 10000
                except IndexError:
                    pass
        return score

    # The minimax algorithm with alpha beta pruning
    # which player 2 uses to decide which column
    # to add a counter
    # used https://medium.com/analytics-vidhya/artificial-intelligence-at-play-connect-four-minimax-algorithm-explained-3b5fc32e4a4f
    # used https://github.com/kupshah/Connect-Four/blob/master/player.py
    def minimax_with_alpha_beta_pruning(self, grid, depth, is_maximizing_player, alpha, beta):
        if self.check_if_game_won(self.__player_1_colour, grid):
            return float('-inf'), None
        elif self.check_if_game_won(self.__player_2_colour, grid):
            return float('inf'), None
        elif depth == 0:
            return self.score_position(self.__player_1_colour, self.__player_2_colour, grid), None
        valid_columns = self.get_valid_columns(grid)
        if is_maximizing_player:
            value = float('-inf')
            best_column = random.choice(valid_columns)
            for column in valid_columns:
                new_grid = []
                for new_column in grid:
                    new_grid.append(new_column[:])
                self.add_counter_to_grid(self.__player_2_colour, new_grid, column)
                new_score = self.minimax_with_alpha_beta_pruning(new_grid, depth-1, False, alpha, beta)[0]
                if new_score > value:
                    value = new_score
                    best_column = column
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value, best_column
        else:
            value = float('inf')
            best_column = random.choice(valid_columns)
            for column in valid_columns:
                new_grid = []
                for new_column in grid:
                    new_grid.append(new_column[:])
                self.add_counter_to_grid(self.__player_1_colour, new_grid, column)
                new_score = self.minimax_with_alpha_beta_pruning(new_grid, depth-1, True, alpha, beta)[0]
                if new_score < value:
                    value = new_score
                    best_column = column
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value, best_column

    # Returns the columns which are not full
    def get_valid_columns(self, grid):
        valid_columns = []
        for x in range(len(grid)):
            if grid[x][len(grid[x]) - 1] == '*':
                valid_columns.append(x)
        return valid_columns

    # Prints a string representation of the grid
    def print_grid(self):
        result = ''
        y = len(self.__grid[0]) - 1
        while y >= 0:
            for x in range(len(self.__grid)):
                result += self.__grid[x][y]
            result += '\n'
            y -= 1
        print(result)

    # Plays the connect4 game
    def __play_game(self):
        # Asks player 1 to choose the colour of the counter
        self.__player_1_colour = 'r'
        self.__player_2_colour = 'y'

        while True:
            if self.__number_of_turns == 0:
                self.print_grid()
                tts.say('it\'s a tie')
                break
            else:
                self.print_grid()
                print('number of turns left: ' + str(self.__number_of_turns) + '\n')
                tts.say(self.__player + '\'s turn\n')

                if self.__player == 'player 1':
                    self.__grid = nao_video_controller.determine_state()

                    if self.check_if_game_won(self.__player_1_colour, self.__grid):
                        self.print_grid()
                        tts.say(self.__player + ' won')
                        break
                    else:
                        self.__player = 'player 2'
                        self.__number_of_turns -= 1

                elif self.__player == 'player 2':
                    hole_number = self.minimax_with_alpha_beta_pruning(self.__grid, 4, True, float('-inf'), float('inf'))[1]
                    nao_motion_controller.wait_for_counter(hole_number)
                    self.add_counter_to_grid(self.__player_2_colour, self.__grid, hole_number)

                    if self.check_if_game_won(self.__player_2_colour, self.__grid):
                        self.print_grid()
                        tts.say(self.__player + ' won')
                        break
                    else:
                        self.__player = 'player 1'
                        self.__number_of_turns -= 1

if __name__ == '__main__':
    Connect4()
