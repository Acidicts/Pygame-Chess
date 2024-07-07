import pygame
from grid import get_grid_square


class Piece:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 80, 80)
        self.image = image
        self.selected = False
        self.moves = 0
        self.grid_x, self.grid_y = get_grid_square((self.x, self.y))
        self.white_moves = []  # This should contain tuples of grid coordinates
        self.black_moves = []  # This should contain tuples of grid coordinates

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        if self.selected:
            self.show_moves(screen)
        self.grid_x, self.grid_y = get_grid_square((self.x, self.y))

    def move(self, pos):
        self.moves += 1
        grid_pos = get_grid_square(pos)
        valid_moves = self.white_moves if self.direction == 1 else self.black_moves
        if grid_pos in valid_moves:
            self.x, self.y = grid_pos[0] * 80, grid_pos[1] * 80
            self.rect.topleft = (self.x, self.y)
            self.first_move = False

    def show_moves(self, screen):
        pass

    def clicked(self, pos):
        return self.rect.collidepoint(pos)

    def destroy(self, screen):
        self.x = -80
        self.y = -80
        self.draw(screen)


class Void(Piece):
    def __init__(self, x, y):
        super().__init__(x, y, None)  # No image for Void spaces
        self.direction = 0  # Void spaces do not have a direction

    def draw(self, screen):
        pass  # Void spaces do not need to be drawn

    def show_moves(self, screen):
        pass  # Void spaces do not have moves

    def move(self, pos):
        pass  # Void spaces cannot move

    def clicked(self, pos):
        return False  # Clicks on Void spaces should not register as selecting a piece


class Pawn(Piece):
    def __init__(self, x, y, image, game):
        super().__init__(x, y, image)
        self.first_move = True
        self.game = game
        self.direction = 0  # Set to 1 for white, -1 for black in the game setup

    def draw(self, screen):
        super().draw(screen)

    def show_moves(self, screen):
        super().show_moves(screen)
        self.white_moves = []
        self.black_moves = []
        self.grid_x, self.grid_y = get_grid_square((self.x, self.y))

        # Forward moves
        forward_move = (self.grid_x, self.grid_y - self.direction)
        double_forward_move = (self.grid_x, self.grid_y - 2 * self.direction)
        forward_moves = [forward_move]
        if self.first_move:
            forward_moves.append(double_forward_move)

        for move in forward_moves:
            blocking_piece = next((p for p in self.game.board if (p.grid_x, p.grid_y) == move), None)
            if not blocking_piece or isinstance(blocking_piece, Void):
                if self.direction == 1:
                    self.white_moves.append(move)
                else:
                    self.black_moves.append(move)

        # Diagonal captures and en passant
        for board_piece in self.game.board:
            piece_grid_x, piece_grid_y = get_grid_square((board_piece.x, board_piece.y))
            if self.direction == 1 and board_piece.direction == -1:
                self.check_diagonal_and_en_passant(piece_grid_x, piece_grid_y, board_piece, True)
            elif self.direction == -1 and board_piece.direction == 1:
                self.check_diagonal_and_en_passant(piece_grid_x, piece_grid_y, board_piece, False)

        # Visualize moves
        for move in self.white_moves + self.black_moves:
            pygame.draw.circle(screen, (0, 255, 0), ((move[0] * 80) + 40, (move[1] * 80) + 40), 10)

    def move(self, pos):
        grid_pos = get_grid_square(pos)
        valid_moves = self.white_moves if self.direction == 1 else self.black_moves
        if grid_pos in valid_moves:
            enemy_piece = next(
                (p for p in self.game.board if (p.grid_x, p.grid_y) == grid_pos and p.direction != self.direction),
                None)
            if enemy_piece:
                self.game.board = [p for p in self.game.board if p != enemy_piece]
            elif self.is_en_passant_move(grid_pos):
                self.handle_en_passant_capture(grid_pos)
            self.x, self.y = grid_pos[0] * 80, grid_pos[1] * 80
            self.rect.topleft = (self.x, self.y)
            self.first_move = False
            self.game.update_last_move(self, (self.grid_x, self.grid_y), grid_pos)

    def is_en_passant_move(self, grid_pos):
        last_move = self.game.last_move
        if last_move and isinstance(last_move[0], Pawn) and abs(last_move[1][1] - last_move[2][1]) == 2:
            if (last_move[2][0], last_move[2][1] - self.direction) == grid_pos:
                return True
        return False

    def handle_en_passant_capture(self, grid_pos):
        last_move = self.game.last_move
        if last_move:
            captured_pawn_pos = (last_move[2][0], last_move[2][1])
            self.game.board = [p for p in self.game.board if not (p.grid_x, p.grid_y) == captured_pawn_pos]

    def check_diagonal_and_en_passant(self, piece_grid_x, piece_grid_y, board_piece, is_white):
        # Diagonal capture
        if piece_grid_x == self.grid_x - 1 and piece_grid_y == self.grid_y - self.direction:
            self.add_move(is_white, piece_grid_x, piece_grid_y)
        elif piece_grid_x == self.grid_x + 1 and piece_grid_y == self.grid_y - self.direction:
            self.add_move(is_white, piece_grid_x, piece_grid_y)

        # En passant
        last_move = self.game.last_move
        if last_move and isinstance(last_move[0], Pawn) and abs(last_move[1][1] - last_move[2][1]) == 2:
            if last_move[2][0] == piece_grid_x and self.grid_y == piece_grid_y:
                en_passant_target = (piece_grid_x, piece_grid_y - self.direction)
                self.add_move(is_white, *en_passant_target)

    def add_move(self, is_white, x, y):
        if is_white:
            self.white_moves.append((x, y))
        else:
            self.black_moves.append((x, y))
