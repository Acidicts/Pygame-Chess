import pygame

class Piece():
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.selected = False

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
        if self.selected:
            self.show_moves()

    def move(self, x, y):
        self.x = x
        self.y = y

    def show_moves(self):
        pass

    def clicked(self, x, y):
        return self.x <= x <= self.x + self.image.get_width() and self.y <= y <= self.y + self.image.get_height()

class Void(Piece):
    def __init__(self, x, y):
        super().__init__(x, y, None)

    def draw(self, screen):
        pass

class Pawn(Piece):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
        self.first_move = True

    def show_moves(self):
        pygame.draw.circle(screen, (0, 255, 0), (self.x + 40, self.y + 40), 10)
        pygame.draw.circle(screen, (255, 0, 0), (self.x + 40, self.y + 120), 10)

