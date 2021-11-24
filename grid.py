# The Grid class which represents a grid in connect 4
import random


class Grid:

    # The constructor of the grid class
    def __init__(self, grid=None,  number_of_counters_in_columns=None):
        # The grid attribute which represents a grid which contains counters,
        # the string '*' represents no counter, the string 'r' represents a
        # red counter, the string 'y' represents a yellow counter
        if grid is None:
            self.__grid = [['*' for y in range(6)] for y in range(7)]
        else:
            self.__grid = grid
        # The number_of_counters_in_columns is a list which keeps track
        # of how many counters each column has, the index represents the column
        # number, the value of the list in each index represents the number
        # of counters in the column number corresponding to the index
        if number_of_counters_in_columns is None:
            self.__number_of_counters_in_columns = [0 for x in range(7)]
        else:
            self.__number_of_counters_in_columns = number_of_counters_in_columns

    # Adds a counter to the grid based on the colour of the counter
    # and upper hole number
    def add_counter_to_grid(self, colour, hole_number):
        self.__grid[hole_number][self.__number_of_counters_in_columns[hole_number]] = colour
        self.__number_of_counters_in_columns[hole_number] += 1

    # Checks if a player has won the game based on the colour of the counter
    def check_if_game_won(self, colour, grid=None):
        if grid is None:
            grid = self.__grid
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
    def minimax_with_alpha_beta_pruning(self, grid, number_of_turns, is_maximizing_player, alpha, beta, player_1_colour, player_2_colour):
        if self.check_if_game_won(player_1_colour, grid):
            return float('-inf'), None
        elif self.check_if_game_won(player_2_colour, grid):
            return float('inf'), None
        elif number_of_turns == 0:
            return self.score_position(player_1_colour, player_2_colour, grid), None
        valid_columns = self.get_valid_columns(grid)
        if is_maximizing_player:
            value = float('-inf')
            best_column = random.choice(valid_columns)
            for column in valid_columns:
                new_grid = []
                for new_column in grid:
                    new_grid.append(new_column[:])
                for y in range(len(new_grid[column])):
                    if new_grid[column][y] == '*':
                        new_grid[column][y] = player_2_colour
                        break
                new_score = self.minimax_with_alpha_beta_pruning(new_grid, number_of_turns-1, False, alpha, beta, player_1_colour, player_2_colour)[0]
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
                for y in range(len(new_grid[column])):
                    if new_grid[column][y] == '*':
                        new_grid[column][y] = player_2_colour
                        break
                new_score = self.minimax_with_alpha_beta_pruning(new_grid, number_of_turns - 1, True, alpha, beta, player_1_colour, player_2_colour)[0]
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

    # Returns the grid attribute
    def get_grid(self):
        return self.__grid

    # Returns the number_of_counters_in_columns attribute
    def get_number_of_counters_in_columns(self):
        return self.__number_of_counters_in_columns

    # Returns a string representation of the grid
    def __str__(self):
        result = ''
        y = len(self.__grid[0]) - 1
        while y >= 0:
            for x in range(len(self.__grid)):
                result += self.__grid[x][y]
            result += '\n'
            y -= 1
        return result
