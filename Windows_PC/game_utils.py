import sys
import pygame
import numpy as np

from pygame.locals import *

PLAYER = 1  # 1 for HUMAN, 0 for MACHINE

WINDOW_WIDTH = 1000  # width of the program's window, in pixels
WINDOW_HEIGHT = 800  # height in pixels
EMPTY = ""  # an arbitrary but unique value

# colors: R    G    B
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 155, 0)
BLUE  = (0, 50, 255)
BROWN = (174, 94, 0)
RED   = (255, 0, 0)


class Board:

    DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    def __init__(self, width, height, space_size):
        # Creates a brand new, empty board data structure.
        self.board = []
        self.turns = 0
        self.time = 0
        self.width, self.height = width, height
        self.space_size = space_size
        self.x_margin = int(int((WINDOW_WIDTH - (width * space_size)) / 2) / 3)
        self.y_margin = int((WINDOW_HEIGHT - (height * space_size)) / 2)
        self.grid_line_color = BLUE
        for i in range(self.width):
            self.board.append([EMPTY] * self.height)
        return

    def add_players(self, player1, player2):
        self.board[player1["rigid1"][0]][player1["rigid1"][1]] = "A"
        self.board[player1["rigid2"][0]][player1["rigid2"][1]] = "B"
        self.board[player2["rigid3"][0]][player2["rigid3"][1]] = "a"
        self.board[player2["rigid4"][0]][player2["rigid4"][1]] = "b"

    def draw_item(self, text, x, y, color):
        large_text = pygame.font.Font('freesansbold.ttf', 30)
        text_surf = large_text.render(text, True, color)
        text_rect = text_surf.get_rect()
        text_rect.center = ((self.space_size / 2) + self.x_margin + x * self.space_size, (self.space_size / 2) +
                           self.y_margin + y * self.space_size)
        self.DISPLAYSURF.blit(text_surf, text_rect)

    def draw_text(self, text, x, y, color):
        large_text = pygame.font.Font('freesansbold.ttf', 30)
        text_surf = large_text.render(text, True, color)
        text_rect = text_surf.get_rect()
        text_rect.center = (x, y)
        self.DISPLAYSURF.blit(text_surf, text_rect)

    def draw_board(self):
        pygame.init()
        pygame.display.set_caption('Crazy Hell Game')

        # the color of the board is blue on the human player's turn, and red on the computer's turn
        self.grid_line_color = BLUE if PLAYER else RED

        font = pygame.font.Font('freesansbold.ttf', 16)
        bigfont = pygame.font.Font('freesansbold.ttf', 32)

        # Draw grid lines of the board.
        for x in range(self.board_width + 1):
            # Draw the horizontal lines.
            start_x = (x * self.space_size) + self.x_margin
            start_y = self.y_margin
            end_x = (x * self.space_size) + self.x_margin
            end_y = self.y_margin + (self.board_height * self.space_size)
            pygame.draw.line(self.DISPLAYSURF, self.grid_line_color, (start_x, start_y), (end_x, end_y))
        for y in range(self.board_height + 1):
            # Draw the vertical lines.
            start_x = self.x_margin
            start_y = (y * self.space_size) + self.y_margin
            end_x = self.x_margin + (self.board_width * self.space_size)
            end_y = (y * self.space_size) + self.y_margin
            pygame.draw.line(self.DISPLAYSURF, self.grid_line_color, (start_x, start_y), (end_x, end_y))

        # Add starting pieces to the center
        for i in range(self.board_width):
            for j in range(self.board_height):
                if self.board[i][j] != EMPTY:
                    if self.board[i][j].isupper():
                        self.draw_item(self.board[i][j], i, j, WHITE)
                    else:
                        self.draw_item(self.board[i][j], i, j, GREEN)

        # Draw Game Info
        self.draw_text("Turns:  " + str(self.turns), WINDOW_WIDTH * 0.75, self.y_margin, BROWN)
        self.draw_text("Time:  " + str(self.time), WINDOW_WIDTH * 0.75, 2*self.y_margin, BROWN)


class Player:

    def __init__(self, player_type, name, x, y):
        self.type = player_type  # 1 for human, 0 for computer
        self.name = name  # the name of the specific drone - rigid1 for example
        self.loc = [x, y]  # where the player is located on the board
        return
