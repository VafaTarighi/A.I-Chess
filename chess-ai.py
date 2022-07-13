import chess
import pygame
from cairosvg import svg2png

game = chess.Board()

search_depth = int(input("Enter AI search depth: "))

positionCount = None


def minimax_root(depth, game: chess.Board, isMaximisingPlayer):
    newGameMoves = game.legal_moves
    bestMove = -9999
    bestMoveFound = None

    for newGameMove in newGameMoves:
        game.push(newGameMove)
        value = minimax(depth - 1, game, -10000, 10000, not isMaximisingPlayer)
        game.pop()
        if value >= bestMove:
            bestMove = value
            bestMoveFound = newGameMove

    return bestMoveFound


def minimax(depth, game: chess.Board, alpha, beta, isMaximisingPlayer):
    global positionCount
    positionCount += 1

    if depth == 0:
        return -evaluate_board(game)

    newGameMoves = game.legal_moves

    if isMaximisingPlayer:
        bestMove = -9999
        for newGameMove in newGameMoves:
            game.push(newGameMove)
            bestMove = max(bestMove, minimax(depth - 1, game, alpha, beta, not isMaximisingPlayer))
            game.pop()
            alpha = max(alpha, bestMove)
            if beta <= alpha:
                return bestMove

        return bestMove
    else:
        bestMove = 9999
        for newGameMove in newGameMoves:
            game.push(newGameMove)
            bestMove = min(bestMove, minimax(depth - 1, game, alpha, beta, not isMaximisingPlayer))
            game.pop()
            beta = min(beta, bestMove)
            if beta <= alpha:
                return bestMove

        return bestMove


def evaluate_board(game: chess.Board):
    totalEvaluation = 0
    for i in range(8):
        for j in range(8):
            square = chess.Square(i * 8 + j)
            totalEvaluation += get_piece_value(game.piece_at(square), i, j)

    return totalEvaluation


def reverse_list(List: list):
    tsil = List.copy()
    tsil.reverse()
    return tsil


pawnEvalWhite = [
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
    [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
    [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
    [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
    [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
    [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
]

pawnEvalBlack = reverse_list(pawnEvalWhite)

knightEval = [
    [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
    [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
    [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
    [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
    [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
    [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
    [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
    [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
]

bishopEvalWhite = [
    [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
    [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
    [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
    [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
    [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
    [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
    [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
    [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
]

bishopEvalBlack = reverse_list(bishopEvalWhite)

rookEvalWhite = [
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
    [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
    [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0]
]

rookEvalBlack = reverse_list(rookEvalWhite)

evalQueen = [
    [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
    [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
    [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
    [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
    [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
    [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
    [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
    [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
]

kingEvalWhite = [

    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
    [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
    [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
    [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
    [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0]
]

kingEvalBlack = reverse_list(kingEvalWhite)


def get_piece_value(piece: chess.Piece, x, y):
    if piece is None:
        return 0

    def get_absolute_value(piece: chess.Piece, isWhite: bool, x, y):
        piece_symbol = piece.symbol().lower()
        if piece_symbol == 'p':
            return 10 + (pawnEvalWhite[y][x] if isWhite else pawnEvalBlack[y][x])

        elif piece_symbol == 'r':
            return 50 + (rookEvalWhite[y][x] if isWhite else rookEvalBlack[y][x])

        elif piece_symbol == 'n':
            return 30 + knightEval[y][x]

        elif piece_symbol == 'b':
            return 30 + (bishopEvalWhite[y][x] if isWhite else bishopEvalBlack[y][x])

        elif piece_symbol == 'q':
            return 90 + evalQueen[y][x]

        elif piece_symbol == 'k':
            return 900 + (kingEvalWhite[y][x] if isWhite else kingEvalBlack[y][x])

        else:
            raise Exception("Unknown piece type: ", piece_symbol)

    absoluteValue = get_absolute_value(piece, piece.color, x, y)
    return absoluteValue if piece.color else -absoluteValue


def make_best_move():
    bestMove = get_best_move(game)
    game.push(bestMove)

    if game.is_game_over():
        print("GAME OVER")


def get_best_move(game: chess.Board):
    if game.is_game_over():
        print("GAME OVER")
        return None

    global positionCount
    positionCount = 0

    # move time can be calculated here
    bestMove = minimax_root(search_depth, game, True)

    return bestMove


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
