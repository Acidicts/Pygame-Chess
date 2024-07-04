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
        if self.selected:
            grid_pos = get_grid_square(pos)
            valid_moves = self.white_moves if self.direction == 1 else self.black_moves
            for move in valid_moves:
                if grid_pos == move:
                    self.x, self.y = move[0] * 80, move[1] * 80
                    self.rect.topleft = (self.x, self.y)
                    break  # Exit the loop once the move is made

    def show_moves(self, screen):
        pass

    def clicked(self, pos):
        return self.rect.collidepoint(pos)


class Void(Piece):
    def __init__(self, x, y):
        super().__init__(x, y, None)

    def draw(self, screen):
        pass

    def move(self, pos):
        pass


class Pawn(Piece):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.first_move = True
        self.direction = 0
        self.black_moves = [self.rect.center[0], self.y + 40 + 80, self.rect.center[0], self.y + 40 + 160]
        self.white_moves = [self.rect.center[0], self.y + 40 - 80, self.rect.center[0], self.y + 40 - 160]

    def show_moves(self, screen):
        if self.direction == -1:
            pygame.draw.circle(screen, (0, 255, 0), self.moves[0], 10)
            if self.first_move:
                pygame.draw.circle(screen, (0, 255, 0), (self.rect.center[0], self.y + 40 + 160), 10)
        elif self.direction == 1:
            pygame.draw.circle(screen, (0, 255, 0), (self.rect.center[0], self.y + 40 - 80), 10)
            if self.first_move:
                pygame.draw.circle(screen, (0, 255, 0), (self.rect.center[0], self.y + 40 - 160), 10)
