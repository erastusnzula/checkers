import pygame

from settings import Settings


class Board:
    """A class to create a checker's board."""

    def __init__(self, screen):
        """
        :param screen: game window
        """
        self.lower_pieces_left = 12
        self.upper_pieces_left = 12
        self.settings = Settings()
        self.screen = screen
        self.all_pieces = []
        self.piece_selected = None
        self.valid = {}
        self.turn = self.settings.red

    def create_square_boxes(self):
        """
        :return: square boxes.
        """
        for row in range(self.settings.rows):
            for column in range(row % 2, self.settings.rows, 2):
                pygame.draw.rect(self.screen, self.settings.white,
                                 (row * self.settings.size_width, column * self.settings.size_height,
                                  self.settings.size_width, self.settings.size_height))

    def create_pieces_on_board(self):
        """
        :return: player pieces.
        """
        for row in range(self.settings.rows):
            self.all_pieces.append([])
            for column in range(self.settings.columns):
                if column % 2 == (row % 2):
                    if row < 3:
                        self.all_pieces[row].append(Piece(self.screen, row, column, self.settings.blue))
                    elif row > 4:
                        self.all_pieces[row].append(Piece(self.screen, row, column, self.settings.red))
                    else:
                        self.all_pieces[row].append(0)
                else:
                    self.all_pieces[row].append(0)

    def draw(self):
        """
        :return: square boxes with player pieces.
        """
        self.create_square_boxes()
        self.create_pieces_on_board()
        for row in range(self.settings.rows):
            for column in range(self.settings.columns):
                piece = self.all_pieces[row][column]
                if piece:
                    piece.draw_piece()

    def pieces_movement(self, piece, row, column):
        """
        :param piece: piece to move
        :param row: piece row.
        :param column: piece column.
        :return: piece in its new position.
        """
        self.all_pieces[piece.row][piece.column], self.all_pieces[row][column] = self.all_pieces[row][column], \
                                                                                 self.all_pieces[piece.row][
                                                                                     piece.column]
        piece.move_piece(row, column)
        if row == self.settings.rows - 1 or row == 0:
            piece.make_king()
            if piece.color == self.settings.blue:
                self.upper_pieces_left += 1
            else:
                self.lower_pieces_left += 1

    def get_piece(self, row, column):
        """
        :param row:
        :param column:
        :return: piece row and column.
        """
        return self.all_pieces[row][column]

    def select_piece(self, row, column):
        """
        :param row:
        :param column:
        :return:
        """
        if self.piece_selected:
            result = self._move_piece(row, column)
            if result is None:
                self.piece_selected = None
                self.select_piece(row, column)
        piece_selected = self.get_piece(row, column)
        if piece_selected and piece_selected.color == self.turn:
            self.piece_selected = piece_selected
            self.valid = self.get_valid_moves(piece_selected)
            return True
        return False

    def _move_piece(self, row, column):
        """
        :param row:
        :param column:
        :return:
        """
        piece_selected = self.get_piece(row, column)
        if self.piece_selected and piece_selected == 0 and (row, column) in self.valid:
            self.pieces_movement(self.piece_selected, row, column)
            skipped = self.valid[(row, column)]
            if skipped:
                self.remove(skipped)
            self.change_turn()
        else:
            return False
        return True

    def change_turn(self):
        """
        :return: active player.
        """
        self.valid = {}
        if self.turn == self.settings.red:
            self.turn = self.settings.blue
        else:
            self.turn = self.settings.red

    def remove(self, skipped_pieces):
        """
        :param skipped_pieces:
        :return: skipped pieces.
        """
        for piece in skipped_pieces:
            self.all_pieces[piece.row][piece.column] = 0
            if piece:
                if piece.color == self.settings.red:
                    self.lower_pieces_left -= 1
                else:
                    self.upper_pieces_left -= 1

    def get_valid_moves(self, piece_selected):
        moves = {}
        left_side = piece_selected.column - 1
        right_side = piece_selected.column + 1
        row = piece_selected.row

        if piece_selected.color == self.settings.red or piece_selected.king:
            moves.update(self._left_movement(row - 1, max(row - 3, -1), -1, piece_selected.color, left_side))
            moves.update(self._right_movement(row - 1, max(row - 3, -1), -1, piece_selected.color, right_side))
        if piece_selected.color == self.settings.blue or piece_selected.king:
            moves.update(
                self._left_movement(row + 1, min(row + 3, self.settings.rows), 1, piece_selected.color, left_side))
            moves.update(
                self._right_movement(row + 1, min(row + 3, self.settings.rows), 1, piece_selected.color, right_side))

        return moves

    def _left_movement(self, start, stop, step, color, left, skipped=None):
        moves = {}
        last_move = []
        for r in range(start, stop, step):
            if left < 0:
                break
            current = self.all_pieces[r][left]
            if current == 0:
                if skipped and not last_move:
                    break
                elif skipped:
                    moves[(r, left)] = last_move + skipped
                else:
                    moves[(r, left)] = last_move

                if last_move:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, self.settings.rows)
                    moves.update(self._left_movement(r + step, row, step, color, left - 1, skipped=last_move))
                    moves.update(self._right_movement(r + step, row, step, color, left + 1, skipped=last_move))
                break
            elif current.color == color:
                break
            else:
                last_move = [current]

            left -= 1

        return moves

    def _right_movement(self, start, stop, step, color, right, skipped=None):
        moves = {}
        last_move = []
        for r in range(start, stop, step):
            if right >= self.settings.columns:
                break
            current = self.all_pieces[r][right]
            if current == 0:
                if skipped and not last_move:
                    break
                elif skipped:
                    moves[(r, right)] = last_move + skipped
                else:
                    moves[(r, right)] = last_move
                if last_move:
                    if step == -1:
                        row = max(r - 3, 0)
                    else:
                        row = min(r + 3, self.settings.rows)
                    moves.update(self._left_movement(r + step, row, step, color, right - 1, skipped=last_move))
                    moves.update(self._right_movement(r + step, row, step, color, right + 1, skipped=last_move))
                break
            elif current.color == color:
                break
            else:
                last_move = [current]
            right += 1
        return moves

    def draw_valid_moves(self, moves):
        for move in moves:
            row, column = move
            pygame.draw.circle(self.screen, self.settings.bg_color,
                               (column * self.settings.size_height + self.settings.size_height // 2,
                                row * self.settings.size_width + self.settings.size_width // 2), 15)


class Piece:
    """Create the checkers player pieces."""

    def __init__(self, screen, row, column, color):
        """Attributes"""
        self.settings = Settings()
        self.screen = screen
        self.row = row
        self.column = column
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calculate_position()

    def calculate_position(self):
        self.x = self.settings.size_width * self.column + self.settings.size_width // 2
        self.y = self.settings.size_height * self.row + self.settings.size_height // 2

    def draw_piece(self):
        pygame.draw.circle(self.screen, self.settings.grey, (self.x, self.y), self.settings.size_width // 2.4)
        pygame.draw.circle(self.screen, self.color, (self.x, self.y), self.settings.size_width // 2.8)
        if self.king:
            self.screen.blit(self.settings.king_icon, (
                self.x - self.settings.king_icon.get_width() / 2, (self.y - self.settings.king_icon.get_height() / 2)))

    def make_king(self):
        self.king = True

    def move_piece(self, row, column):
        self.row = row
        self.column = column
        self.calculate_position()
