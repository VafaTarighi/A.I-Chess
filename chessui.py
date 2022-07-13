from chessai import *

import pygame
from cairosvg import svg2png

pygame.init()
window = pygame.display.set_mode((390, 390))


def draw_board():
    svg2png(bytestring=game._repr_svg_(), write_to='board.png')
    img = pygame.image.load('board.png')
    window.blit(img, (0, 0))
    pygame.display.update()


draw_board()


def find_piece_pos(x, y):
    x_sym = chr(ord('a') + int(x / 45)) if x > 0 else 'a'
    y_sym = 1 + int(y / 45) if y > 0 else 1

    if x_sym == 'i':
        x_sym = chr(ord(x_sym) - 1)

    if y_sym == 9:
        y_sym -= 1

    return x_sym + str(y_sym)


is_selected = False
selected_piece = None


def color_selection(x, y):
    rect = pygame.Surface((45, 45))
    rect.set_alpha(32)
    rect.fill((0, 255, 0))
    x_board = 15 + 45 * int((x - 15) / 45)
    y_board = 15 + 45 * int((y - 15) / 45)
    window.blit(rect, (x_board, y_board))
    pygame.display.update()


while not game.is_game_over():
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)

        elif event.type == pygame.MOUSEBUTTONUP:

            x, y = pygame.mouse.get_pos()
            piece_pos = find_piece_pos(x - 15, 390 - y - 15)
            print(piece_pos)

            if is_selected:
                if selected_piece == piece_pos:
                    is_selected = False
                    draw_board()
                    continue

                my_move = chess.Move.from_uci(selected_piece + piece_pos)
                if my_move in game.legal_moves:
                    game.push(my_move)
                    draw_board()
                    is_selected = False

                    make_best_move()
                    draw_board()

                else:
                    is_selected = False
                    draw_board()

            else:
                for move in game.legal_moves:
                    if move.uci().startswith(piece_pos):
                        print(move)
                        is_selected = True
                        selected_piece = piece_pos
                        color_selection(x, y)
