import chess

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
