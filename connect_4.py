# The Connect4 class which represents the connect4 game
from __future__ import division
import numpy as np
import cv2
import naoqi
import numpy as np
import random
import keyboard
import time
from PIL import Image

posture_proxy = naoqi.ALProxy("ALRobotPosture", "192.168.94.75", 9559)
posture_proxy.goToPosture("Stand", 1.0)
HEAD_CHAIN = ["HeadPitch", "HeadYaw"]
FACING_FORWARD = [0, 0]
RIGHT_ARM_CHAIN = ["RShoulderPitch", "RShoulderRoll", "RElbowRoll", "RElbowYaw", "RWristYaw"]
LEFT_ARM_CHAIN = ["LShoulderPitch", "LShoulderRoll", "LElbowRoll", "LElbowYaw", "LWristYaw"]
RAISED = [-1.22, 0.05, -0.55, -1.29, -0.77]
RED_LEDS = [
            "Face/Led/Red/Left/0Deg/Actuator/Value",
            "Face/Led/Red/Left/45Deg/Actuator/Value",
            "Face/Led/Red/Left/90Deg/Actuator/Value",
            "Face/Led/Red/Left/135Deg/Actuator/Value",
            "Face/Led/Red/Left/180Deg/Actuator/Value",
            "Face/Led/Red/Left/225Deg/Actuator/Value",
            "Face/Led/Red/Left/270Deg/Actuator/Value",
            "Face/Led/Red/Left/315Deg/Actuator/Value",
            "Face/Led/Red/Right/0Deg/Actuator/Value",
            "Face/Led/Red/Right/45Deg/Actuator/Value",
            "Face/Led/Red/Right/90Deg/Actuator/Value",
            "Face/Led/Red/Right/135Deg/Actuator/Value",
            "Face/Led/Red/Right/180Deg/Actuator/Value",
            "Face/Led/Red/Right/225Deg/Actuator/Value",
            "Face/Led/Red/Right/270Deg/Actuator/Value",
            "Face/Led/Red/Right/315Deg/Actuator/Value"]
GREEN_LEDS = [
            "Face/Led/Green/Left/0Deg/Actuator/Value",
            "Face/Led/Green/Left/45Deg/Actuator/Value",
            "Face/Led/Green/Left/90Deg/Actuator/Value",
            "Face/Led/Green/Left/135Deg/Actuator/Value",
            "Face/Led/Green/Left/180Deg/Actuator/Value",
            "Face/Led/Green/Left/225Deg/Actuator/Value",
            "Face/Led/Green/Left/270Deg/Actuator/Value",
            "Face/Led/Green/Left/315Deg/Actuator/Value",
            "Face/Led/Green/Right/0Deg/Actuator/Value",
            "Face/Led/Green/Right/45Deg/Actuator/Value",
            "Face/Led/Green/Right/90Deg/Actuator/Value",
            "Face/Led/Green/Right/135Deg/Actuator/Value",
            "Face/Led/Green/Right/180Deg/Actuator/Value",
            "Face/Led/Green/Right/225Deg/Actuator/Value",
            "Face/Led/Green/Right/270Deg/Actuator/Value",
            "Face/Led/Green/Right/315Deg/Actuator/Value"]
RED_LEDS_NAME = "red leds"
GREEN_LEDS_NAME = "green leds"

class Connect4:

    # The constructor of the Connect4 class
    def __init__(self, ip_address, port):
        self.__tts = naoqi.ALProxy("ALTextToSpeech", ip_address, port)
        self.__camera_proxy = naoqi.ALProxy("ALVideoDevice", ip_address, port)
        self.__memory = naoqi.ALProxy("ALMemory", ip_address, port)
        self.__face_characteristics = naoqi.ALProxy("ALFaceCharacteristics", ip_address, port)
        self.__motion = naoqi.ALProxy("ALMotion", ip_address, port)
        self.__leds = naoqi.ALProxy("ALLeds", ip_address, port)
        self.__leds.createGroup(RED_LEDS_NAME, RED_LEDS)
        self.__leds.createGroup(GREEN_LEDS_NAME, GREEN_LEDS)
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
        # The difficulty attribute which represents the difficulty of the game
        self.__difficulty = "medium"
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

    # Determines which hole number to put the
    # counter in based on the difficulty
    def determine_hole_number(self):
        hole_number = 0
        if self.__difficulty == "easy":
            hole_number = self.minimax_with_alpha_beta_pruning(self.__grid, 1, True, float('-inf'), float('inf'))[1]
        elif self.__difficulty == "medium":
            if random.random() > 0.5:
                hole_number = self.minimax_with_alpha_beta_pruning(self.__grid, 2, True, float('-inf'), float('inf'))[1]
            else:
                hole_number = random.choice(self.get_valid_columns(self.__grid))
        elif self.__difficulty == "hard":
            hole_number = self.minimax_with_alpha_beta_pruning(self.__grid, 2, True, float('-inf'), float('inf'))[1]
        return hole_number

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

    # Uses the persons facial expression to adjust
    # the difficulty of the game
    def adjust_difficulty(self, facial_expression):
        if self.__difficulty == 'easy':
            if facial_expression == 'happy':
                self.__difficulty = 'medium'
            self.__tts.say('the difficulty is now ' + self.__difficulty)
        elif self.__difficulty == 'medium':
            if facial_expression == 'anger' \
            or facial_expression == 'surprise' \
            or facial_expression == 'disgust' \
            or facial_expression == 'fear' \
            or facial_expression == 'sad':
                self.__difficulty = 'easy'
            elif facial_expression == 'happy':
                self.__difficulty = 'hard'
            self.__tts.say('the difficulty is now ' + self.__difficulty)
        elif self.__difficulty == 'hard':
            if facial_expression == 'anger' \
            or facial_expression == 'surprise'\
            or facial_expression == 'disgust' \
            or facial_expression == 'fear' \
            or facial_expression == 'sad':
                self.__difficulty = 'medium'
            self.__tts.say('the difficulty is now ' + self.__difficulty)

    # takes a picture
    def take_picture(self, camera_number, image_name):
        name_id = self.__camera_proxy.subscribeCamera("VM", camera_number, 2, 13, 1)
        self.__motion.angleInterpolation(HEAD_CHAIN, FACING_FORWARD, 2., True)
        nao_image = self.__camera_proxy.getImageRemote(name_id)
        self.__camera_proxy.unsubscribe(name_id)
        image_width = nao_image[0]
        image_height = nao_image[1]
        array = nao_image[6]

        im = Image.frombytes("RGB", (image_width, image_height), array)
        im.save(image_name + ".png", "PNG")

    # programs the NAO robot to react to the game state
    def react_to_game_state(self):
        score = self.score_position(self.__player_1_colour, self.__player_2_colour, self.__grid)
        if score >= 100:
            self.__motion.angleInterpolation(LEFT_ARM_CHAIN, RAISED, 2., True)
            self.__motion.angleInterpolation(LEFT_ARM_CHAIN, RAISED, 2., True)
            self.__tts.say("I am doing great at this game")
            self.__leds.off("FaceLeds")
            self.__leds.on(GREEN_LEDS_NAME)
            time.sleep(5)
            self.__leds.off(GREEN_LEDS_NAME)
            self.__leds.on("FaceLeds")
        elif score <= -100:
            self.__tts.say("Wow you really are great at this game")
            self.__leds.off("FaceLeds")
            self.__leds.on(RED_LEDS_NAME)
            time.sleep(5)
            self.__leds.off(RED_LEDS_NAME)
            self.__leds.on("FaceLeds")

    # determines the state of the game
    # used https://github.com/Matt-Jennings-GitHub/ConnectFour-ComputerVisionAI/blob/master/ConnectFourComputerVision.py
    def determine_state(self):
        # used http://doc.aldebaran.com/1-14/dev/python/examples/vision/get_image.html
        self.take_picture(1, "grid_image")

        img = cv2.imread("grid_image.png")
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

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
                self.__tts.say('it\'s a tie')
                break
            else:
                self.print_grid()
                print('number of turns left: ' + str(self.__number_of_turns) + '\n')
                self.__tts.say(self.__player + '\'s turn\n')

                if self.__player == 'player 1':
                    time.sleep(10)
                    self.__grid = self.determine_state()
                    
                    if self.check_if_game_won(self.__player_1_colour, self.__grid):
                        self.print_grid()
                        self.__tts.say(self.__player + ' won')
                        break
                    else:
                        self.__player = 'player 2'
                        self.__number_of_turns -= 1
                        self.react_to_game_state()

                elif self.__player == 'player 2':
                    hole_number = self.determine_hole_number()
                    self.add_counter_to_grid(self.__player_2_colour, self.__grid, hole_number)

                    player_2_counter_put_in_grid = False
                    while not player_2_counter_put_in_grid:
                        self.__tts.say("please put player 2's counter in hole " + str(7-hole_number))
                        time.sleep(10)

                        new_grid = self.determine_state()
                        if self.__grid == new_grid:
                            player_2_counter_put_in_grid = True
                        else:
                            self.print_grid()
                            self.__tts.say("that is the incorrect hole number, please try again")

                    if self.check_if_game_won(self.__player_2_colour, self.__grid):
                        self.print_grid()
                        self.__tts.say(self.__player + ' won')
                        break
                    else:
                        self.__player = 'player 1'
                        self.__number_of_turns -= 1

                        # used https://stackoverflow.com/questions/24072790/how-to-detect-key-presses
                        print("press q to continue")
                        keyboard.wait('q')
                        print('\n')

                        self.take_picture(0, "face_of_user")

                        # used https://stackoverflow.com/questions/24072790/how-to-detect-key-presses
                        print("press q to continue")
                        keyboard.wait('q')
                        print('\n')

                        #used https://www.geeksforgeeks.org/reading-writing-text-files-python/
                        file = open("facial expression.txt", 'r')
                        lines = file.readlines()
                        facial_expression = lines[0][0:len(lines[0])-2]

                        self.adjust_difficulty(facial_expression)

if __name__ == '__main__':
    Connect4("192.168.94.75", 9559)
