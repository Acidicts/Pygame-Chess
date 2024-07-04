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
            for j in range(7):
                if j == 6:
                    self.board.append(Pawn(i * 80, j * 80, self.white_assets["pawn"]))
                    self.board[-1].direction = 1
                elif j == 1:
                    self.board.append(Pawn(i * 80, j * 80, self.black_assets["pawn"]))
                    self.board[-1].direction = -1
                else:
                    self.board.append(Void(i * 80, j * 80))

    def draw_board(self):
        for i in range(8):
            for j in range(8):
                color = (51, 32, 2) if (i + j) % 2 == 0 else (255, 219, 160)
                pygame.draw.rect(win, color, (i * 80, j * 80, 80, 80))
        pygame.draw.rect(win, (0, 0, 0), (0, 0, 640, 640), 5)

    def run(self):
        running = True
        clock = pygame.time.Clock()
        selected_piece = None  # Track the currently selected piece

        while running:
            clock.tick(60)
            win.fill((255, 255, 255))
            self.draw_board()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if selected_piece:
                        # Move the selected piece to the new location
                        grid_pos = get_grid_square(pos)
                        new_x, new_y = grid_pos[0] * 80, grid_pos[1] * 80
                        selected_piece.x = new_x
                        selected_piece.y = new_y
                        selected_piece.rect.topleft = (new_x, new_y)
                        selected_piece.first_move = False
                        selected_piece.selected = False
                        selected_piece = None  # Deselect the piece after moving
                    else:
                        # Select a piece
                        for piece in self.board:
                            if piece.rect.collidepoint(pos):
                                piece.selected = True
                                selected_piece = piece
                                break  # Stop the loop once the piece is found and selected

            for piece in self.board:
                piece.draw(win)
                if piece.selected:
                    piece.show_moves(win)

            pygame.display.flip()


game = Game()
game.run()
