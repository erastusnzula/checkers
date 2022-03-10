import sys

import pygame

from board import Board
from settings import Settings


class Game:
    """A class to control game functionality."""

    def __init__(self):
        """Game attributes."""
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.width, self.settings.height))
        pygame.display.set_caption('Checkers')
        pygame.display.set_icon(self.settings.icon)
        self.clock = pygame.time.Clock()
        self.board = Board(self.screen)

    def get_position(self, pos):
        """
        :param pos: mouse position
        :return: row and column of a piece based on mouse position.
        """
        x, y = pos
        row = y // self.settings.size_height
        column = x // self.settings.size_width
        return row, column

    def run(self):
        """
        :return: game window.
        """
        while True:
            self.clock.tick(60)
            self._check_events()
            self._update_screen()

    def _check_events(self):
        """
        :return: keyboard and mouse events.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                self._check_mouse_down_events(event)

    def _check_mouse_down_events(self, event):
        """
        :param event: None
        :return: the selected piece.
        """
        pos = pygame.mouse.get_pos()
        row, column = self.get_position(pos)
        self.board.select_piece(row, column)

    def _update_screen(self):
        """
        :return: updated window.
        """
        self.screen.fill(self.settings.bg_color)
        self.board.draw()
        self.board.draw_valid_moves(self.board.valid)
        pygame.display.flip()


my_game = Game()
my_game.run()
