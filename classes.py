import pygame
from grid import get_grid_square

class Piece:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 80, 80)
        self.image = image
        self.selected = False
        self.white_moves = []  # This should contain tuples of grid coordinates
        self.black_moves = []  # This should contain tuples of grid coordinates

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        if self.selected:
            self.show_moves(screen)

    def move(self, pos):
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
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.first_move = True
        self.direction = 0  # Set to 1 for white, -1 for black in the game setup

    def show_moves(self, screen):
        self.white_moves = []
        self.black_moves = []
        grid_x, grid_y = get_grid_square((self.x, self.y))

        if self.direction == 1:  # White pawn
            self.white_moves.append((grid_x, grid_y - 1))
            if self.first_move:
                self.white_moves.append((grid_x, grid_y - 2))
        elif self.direction == -1:  # Black pawn
            self.black_moves.append((grid_x, grid_y + 1))
            if self.first_move:
                self.black_moves.append((grid_x, grid_y + 2))

        for move in self.white_moves + self.black_moves:
            pygame.draw.circle(screen, (0, 255, 0), ((move[0] * 80) + 40, (move[1] * 80) + 40), 10)