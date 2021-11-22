# The Grid class which represents a grid in connect 4
class Grid:

    # The constructor of the grid class
    def __init__(self):
        # The grid attribute which represents a grid which contains counters,
        # the string '*' represents no counter, the string 'r' represents a
        # red counter, the string 'y' represents a yellow counter
        self.__grid = [['*' for y in range(6)] for y in range(7)]
        # The number_of_counters_in_columns is a list which keeps track
        # of how many counters each column has, the index represents the column
        # number, the value of the list in each index represents the number
        # of counters in the column number corresponding to the index
        self.__number_of_counters_in_columns = [0 for x in range(7)]

    # Adds a counter to the grid based on the colour of the counter
    # and upper hole number
    def add_counter_to_grid(self, colour, hole_number):
        self.__grid[hole_number][self.__number_of_counters_in_columns[hole_number]] = colour
        self.__number_of_counters_in_columns[hole_number] += 1

    # Checks if a player has won the game based on the colour of the counter
    def check_if_game_won(self, colour):
        # Checks the horizontal spaces
        for y in range(len(self.__grid[0])):
            for x in range(len(self.__grid) - 3):
                if self.__grid[x][y] == colour and self.__grid[y][y] == colour and self.__grid[x+2][y] == colour and self.__grid[x+3][y] == colour:
                    return True

        # Checks the vertical spaces
        for x in range(len(self.__grid)):
            for y in range(len(self.__grid[0]) - 3):
                if self.__grid[x][y] == colour and self.__grid[x][y+1] == colour and self.__grid[x][y+2] == colour and self.__grid[x][y+3] == colour:
                    return True

        # Checks the positively sloped diagonal spaces
        for x in range(len(self.__grid) - 3):
            for y in range(len(self.__grid[0]) - 3):
                if self.__grid[x][y] == colour and self.__grid[x+1][y+1] == colour and self.__grid[x+2][y+2] == colour and self.__grid[x+3][y+3] == colour:
                    return True

        # Checks the positively sloped diagonal spaces
        for x in range(len(self.__grid) - 3):
            for y in range(len(self.__grid[0]) - 3):
                if self.__grid[x][y] == colour and self.__grid[x+1][y+1] == colour and self.__grid[x+2][y+2] == colour and self.__grid[x+3][y+3] == colour:
                    return True

        # Checks the negatively sloped diagonal spaces
        for x in range(len(self.__grid) - 3):
            for y in range(3, len(self.__grid[0])):
                if self.__grid[x][y] == colour and self.__grid[x+1][y-1] == colour and self.__grid[x+2][y-2] == colour and self.__grid[x+3][y-3] == colour:
                    return True

        return False

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

