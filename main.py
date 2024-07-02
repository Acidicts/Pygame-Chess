import pygame
from pygame import Surface, SurfaceType

from utils import load_image
from classes import *

pygame.init()

pygame.display.set_caption("Chess")
WIDTH, HEIGHT = 640, 700
win = pygame.display.set_mode((WIDTH, HEIGHT))


class Game:
    def __init__(self):
        self.white_assets = {
            "pawn": load_image("white_pawn.png"),
            "rook": load_image("white_rook.png"),
            "knight": load_image("white_knight.png"),
            "bishop": load_image("white_bishop.png"),
            "queen": load_image("white_queen.png"),
            "king": load_image("white_king.png"),
        }
        self.black_assets = {
            "pawn": load_image("black_pawn.png"),
            "rook": load_image("black_rook.png"),
            "knight": load_image("black_knight.png"),
            "bishop": load_image("black_bishop.png"),
            "queen": load_image("black_queen.png"),
            "king": load_image("black_king.png"),
        }
        self.board = []
        for i in range(8):
            for j in range(8):
                self.board.append(Void(i * 80, j * 80))
        for tile in self.board:
            tile = Pawn(0, self.board.index(tile) * 80, self.white_assets["pawn"])

    def draw_board(self):
        for i in range(8):
            for j in range(8):
                color = (51, 32, 2) if (i + j) % 2 == 0 else (255, 219, 160)
                pygame.draw.rect(win, color, (i * 80, j * 80, 80, 80))
        pygame.draw.rect(win, (0, 0, 0), (0, 0, 640, 640), 5)

    def run(self):
        running = True
        while running:

            win.fill((255, 255, 255))
            self.draw_board()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            for piece in self.board:
                try:
                    piece.draw(win)
                finally:
                    pass

            win.blit(self.white_assets['pawn'], (0, 560))

            pygame.display.update()


game = Game()
game.run()
