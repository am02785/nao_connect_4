# The Connect4 class which represents the connect4 game
import math
import cv2
import numpy as np
import random
import nao_motion_controller

# determines the state of the game
def determine_state():
    img = cv2.imread('picture2.png')

    new_width = 500  # Resize
    img_h, img_w, _ = img.shape
    scale = new_width / img_w
    img_w = int(img_w * scale)
    img_h = int(img_h * scale)
    img = cv2.resize(img, (img_w, img_h), interpolation=cv2.INTER_AREA)
    img_orig = img.copy()

    # Bilateral Filter
    bilateral_filtered_image = cv2.bilateralFilter(img, 15, 190, 190)

    # Outline Edges
    edge_detected_image = cv2.Canny(bilateral_filtered_image, 75, 150)

    # Find Circles
    ret, contours, hierarchy = cv2.findContours(edge_detected_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # Edges to contours

    contour_list = []
    rect_list = []
    position_list = []

    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)  # Contour Polygons
        area = cv2.contourArea(contour)

        rect = cv2.boundingRect(contour)  # Polygon bounding rectangles
        x_rect, y_rect, w_rect, h_rect = rect
        x_rect += w_rect / 2
        y_rect += h_rect / 2
        area_rect = w_rect * h_rect

        if ((len(approx) > 8) & (len(approx) < 23) & (area > 250) & (area_rect < (img_w * img_h) / 5)) & (
                w_rect in range(h_rect - 10, h_rect + 10)):  # Circle conditions
            contour_list.append(contour)
            position_list.append((x_rect, y_rect))
            rect_list.append(rect)

    img_circle_contours = img_orig.copy()
    cv2.drawContours(img_circle_contours, contour_list, -1, (0, 255, 0), thickness=1)  # Display Circles
    for rect in rect_list:
        x, y, w, h = rect
        cv2.rectangle(img_circle_contours, (x, y), (x + w, y + h), (0, 0, 255), 1)

    # Interpolate Grid
    rows, cols = (6, 7)
    mean_w = sum([rect[2] for r in rect_list]) / len(rect_list)
    mean_h = sum([rect[3] for r in rect_list]) / len(rect_list)
    position_list.sort(key=lambda x: x[0])
    max_x = int(position_list[-1][0])
    min_x = int(position_list[0][0])
    position_list.sort(key=lambda x: x[1])
    max_y = int(position_list[-1][1])
    min_y = int(position_list[0][1])
    grid_width = max_x - min_x
    grid_height = max_y - min_y
    col_spacing = int(grid_width / (cols - 1))
    row_spacing = int(grid_height / (rows - 1))

    # Find Colour Masks
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)  # Convert to HSV space

    lower_red = np.array([150, 150, 100])  # Lower range for red colour space
    upper_red = np.array([255, 255, 255])  # Upper range for red colour space
    mask_red = cv2.inRange(img_hsv, lower_red, upper_red)
    img_red = cv2.bitwise_and(img, img, mask=mask_red)

    lower_yellow = np.array([10, 150, 100])
    upper_yellow = np.array([60, 255, 255])
    mask_yellow = cv2.inRange(img_hsv, lower_yellow, upper_yellow)
    img_yellow = cv2.bitwise_and(img, img, mask=mask_yellow)

    # Identify Colours
    grid = np.zeros((rows, cols))
    id_red = 1
    id_yellow = -1
    img_grid_overlay = img_orig.copy()
    img_grid = np.zeros([img_h, img_w, 3], dtype=np.uint8)

    for x_i in range(0, cols):
        x = int(min_x + x_i * col_spacing)
        for y_i in range(0, rows):
            y = int(min_y + y_i * row_spacing)
            r = int((mean_h + mean_w) / 5)
            img_grid_circle = np.zeros((img_h, img_w))
            cv2.circle(img_grid_circle, (x, y), r, (255, 255, 255), thickness=-1)
            img_res_red = cv2.bitwise_and(img_grid_circle, img_grid_circle, mask=mask_red)
            img_grid_circle = np.zeros((img_h, img_w))
            cv2.circle(img_grid_circle, (x, y), r, (255, 255, 255), thickness=-1)
            img_res_yellow = cv2.bitwise_and(img_grid_circle, img_grid_circle, mask=mask_yellow)
            cv2.circle(img_grid_overlay, (x, y), r, (0, 255, 0), thickness=1)
            if img_res_red.any() != 0:
                grid[y_i][x_i] = id_red
                cv2.circle(img_grid, (x, y), r, (0, 0, 255), thickness=-1)
            elif img_res_yellow.any() != 0:
                grid[y_i][x_i] = id_yellow
                cv2.circle(img_grid, (x, y), r, (0, 255, 255), thickness=-1)

    state = []
    for x in range(7):
        column = []
        for y in range(6):
            if grid[5-y][x] == id_red:
                column.append('r')
            elif grid[5-y][x] == id_yellow:
                column.append('y')
            else:
                column.append('*')
        state.append(column)

    return state

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
        self.__player_1_colour = raw_input("Enter which colour you want to use:")
        if self.__player_1_colour == 'r':
            self.__player_2_colour = 'y'
        elif self.__player_1_colour == 'y':
            self.__player_2_colour = 'r'
        else:
            raise Exception()
        print('\n')

        while True:
            if self.__number_of_turns == 0:
                self.print_grid()
                print('it\'s a tie')
                break
            else:
                self.print_grid()
                print('number of turns left: ' + str(self.__number_of_turns) + '\n')
                print(self.__player + '\'s turn\n')

                if self.__player == 'player 1':
                    self.__grid = determine_state()

                    if self.check_if_game_won(self.__player_1_colour, self.__grid):
                        self.print_grid()
                        print(self.__player + ' won')
                        print('\n')
                        break
                    else:
                        self.__player = 'player 2'
                        self.__number_of_turns -= 1

                elif self.__player == 'player 2':
                    hole_number = self.minimax_with_alpha_beta_pruning(self.__grid, 4, True, float('-inf'), float('inf'))[1]
                    nao_motion_controller.wait_for_counter(hole_number)
                    print('\n')
                    self.add_counter_to_grid(self.__player_2_colour, self.__grid, hole_number)
                    if self.check_if_game_won(self.__player_2_colour, self.__grid):
                        self.print_grid()
                        print(self.__player + ' won')
                        print('\n')
                        break
                    else:
                        self.__player = 'player 1'
                        self.__number_of_turns -= 1

if __name__ == '__main__':
    Connect4()
