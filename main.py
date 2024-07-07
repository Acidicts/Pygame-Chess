import pygame
from pygame import Surface, SurfaceType

from utils import load_image
from classes import *

pygame.init()


class Game:
    def __init__(self):
        pygame.display.set_caption("Chess")
        WIDTH, HEIGHT = 640, 700
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))

        self.last_move = None

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
                    self.board.append(Pawn(i * 80, j * 80, self.white_assets["pawn"], self))
                    self.board[-1].direction = 1
                elif j == 1:
                    self.board.append(Pawn(i * 80, j * 80, self.black_assets["pawn"], self))
                    self.board[-1].direction = -1
                else:
                    self.board.append(Void(i * 80, j * 80))

    def update_last_move(self, piece, old_pos, new_pos):
        self.last_move = (piece, old_pos, new_pos)

    def draw_board(self):
        for i in range(8):
            for j in range(8):
                color = (51, 32, 2) if (i + j) % 2 == 0 else (255, 219, 160)
                pygame.draw.rect(self.win, color, (i * 80, j * 80, 80, 80))
        pygame.draw.rect(self.win, (0, 0, 0), (0, 0, 640, 640), 5)

    def run(self):
        running = True
        clock = pygame.time.Clock()
        selected_piece = None  # Track the currently selected piece

        while running:
            clock.tick(60)
            self.win.fill((255, 255, 255))
            self.draw_board()

            for piece in self.board:
                piece.draw(self.win)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    pos = pygame.mouse.get_pos()
                    clicked_piece = None
                    for piece in self.board:
                        if piece.clicked(pos):
                            clicked_piece = piece
                            break

                    if selected_piece and clicked_piece == selected_piece:
                        selected_piece.selected = False
                        selected_piece = None
                    elif clicked_piece and not selected_piece:
                        clicked_piece.selected = True
                        selected_piece = clicked_piece
                    elif selected_piece:
                        # Validate and move the selected piece to the new location
                        grid_pos = get_grid_square(pos)
                        if grid_pos in selected_piece.white_moves or grid_pos in selected_piece.black_moves:
                            selected_piece.move(pos)
                            selected_piece.selected = False
                            selected_piece = None

            for piece in self.board:
                if piece.selected:
                    piece.show_moves(self.win)

            pygame.display.update()

game = Game()
game.run()
