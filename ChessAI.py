"""
Handling AI moves.
"""
import random
import numpy as np

piece_score = {"K": 10000, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}

knight_scores =[[-0.50,-0.40,-0.30,-0.30,-0.30,-0.30,-0.40, -0.50],
                [-0.40,-0.20,    0,    0,    0,    0,-0.20, -0.40],
                [-0.30,    0, 0.10, 0.15, 0.15, 0.10,    0, -0.30],
                [-0.30, 0.05, 0.15, 0.20, 0.20, 0.15, 0.05, -0.30],
                [-0.30,    0, 0.15, 0.20, 0.20, 0.15,    0, -0.30],
                [-0.30, 0.05, 0.10, 0.15, 0.15, 0.10, 0.05,   -30],
                [-0.40,-0.20,    0, 0.05, 0.05,    0,-0.20, -0.40],
                [-0.50,-0.40,-0.30,-0.30,-0.30,-0.30,-0.40, -0.50]]

bishop_scores =[[-0.20,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.20],
                [-0.10,  0,  0,  0,  0,  0,  0,-0.10],
                [-0.10,  0,  0.05, 0.10, 0.10,  0.05,  0,-0.10],
                [-0.10,  0.05,  0.05, 0.10, 0.10,  0.05,  0.05,-0.10],
                [-0.10,  0, 0.10, 0.10, 0.10, 0.10,  0,-0.10],
                [-0.10, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10,-0.10],
                [-0.10,  0.05,  0,  0,  0,  0,  0.05,-0.10],
                [-0.20,-0.10,-0.10,-0.10,-0.10,-0.10,-0.10,-0.20]]

rook_scores =  [[0,  0,  0,  0,  0,  0,  0,  0],
                [0.05, 0.10, 0.10, 0.10, 0.10, 0.10, 0.10,  0.05],
                [-0.05,  0,  0,  0,  0,  0,  0, -0.05],
                [-0.05,  0,  0,  0,  0,  0,  0, -0.05],
                [-0.05,  0,  0,  0,  0,  0,  0, -0.05],
                [-0.05,  0,  0,  0,  0,  0,  0, -0.05],
                [-0.05,  0,  0,  0,  0,  0,  0, -0.05],
                [0,  0,  0,  0.05,  0.05,  0,  0,  0]]

queen_scores = [[-0.20,-0.10,-0.10, -0.5, -0.5,-0.10,-0.10,-0.20],
                [-0.10,  0,  0,  0,  0,  0,  0,-0.10],
                [-0.10,  0,  0.05,  0.05,  0.05,  0.05,  0,-0.10],
                [-0.05,  0,  0.05,  0.05,  0.05,  0.05,  0, -0.05],
                [0,  0,  0.05,  0.05,  0.05,  0.05,  0, -0.05],
                [-0.10,  0.05,  0.05,  0.05,  0.05,  0.05,  0,-0.10],
                [-0.10,  0,  0.05,  0,  0,  0,  0,-0.10],
                [-0.20,-0.10,-0.10, -0.05, -0.05,-0.10,-0.10,-0.20]]

pawn_scores = [ [0,  0,  0,  0,  0,  0,  0,  0],
                [0.50, 0.50, 0.50, 0.50, 0.50, 0.50, 0.50, 0.50],
                [0.10, 0.10, 0.20, 0.30, 0.30, 0.20, 0.10, 0.10],
                [0.05,  0.05, 0.10, 0.25, 0.25, 0.10,  0.05,  0.05],
                [0,  0,  0, 0.20, 0.20,  0,  0,  0],
                [0.05, -0.05,-0.10,  0,  0,-0.10, -0.05,  0.05],
                [0.05, 0.10, 0.10,-0.20,-0.20, 0.10, 0.10,  0.05],
                [0,  0,  0,  0,  0,  0,  0,  0]]

king_scores=[[-0.3,-0.4,-0.4,-0.5,-0.5,-0.4,-0.4,-0.3],
             [-0.3,-0.4,-0.4,-0.5,-0.5,-0.4,-0.4,-0.3],
             [-0.3,-0.4,-0.4,-0.5,-0.5,-0.4,-0.4,-0.3],
             [-0.3,-0.4,-0.4,-0.5,-0.5,-0.4,-0.4,-0.3],
             [-0.2,-0.3,-0.3,-0.4,-0.4,-0.3,-0.3,-0.2],
             [-0.1,-0.2,-0.2,-0.2,-0.2,-0.2,-0.2,-0.1],
             [0.20, 0.20,  0,  0,  0,  0,0.20, 0.20],
             [0.20, 0.30, 0.10,  0,  0, 0.10, 0.30, 0.20]]




piece_position_scores = {"wN": knight_scores,
                         "bN": knight_scores[::-1],
                         "wB": bishop_scores,
                         "bB": bishop_scores[::-1],
                         "wQ": queen_scores,
                         "bQ": queen_scores[::-1],
                         "wR": rook_scores,
                         "bR": rook_scores[::-1],
                         "wp": pawn_scores,
                         "bp": pawn_scores[::-1],
                         "wK": king_scores,
                         "bK": king_scores[::-1],}


CHECKMATE = float("inf")
STALEMATE = 0
DEPTH = 4


def findBestMove(game_state, valid_moves, return_queue):
    global next_move
    next_move = None
    random.shuffle(valid_moves)
    findMoveNegaMaxAlphaBeta(game_state, valid_moves, DEPTH, -CHECKMATE, CHECKMATE,
                             1 if game_state.white_to_move else -1)
    return_queue.put(next_move)


def findMoveNegaMaxAlphaBeta(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
    global next_move
    if depth == 0:
        return turn_multiplier * scoreBoard(game_state)
    #move ordering - improve later //TODO
    valid_moves=ordermoves(valid_moves)

    max_score = -CHECKMATE
    for move in valid_moves:
        game_state.makeMove(move)
        next_moves = game_state.getValidMoves()
        score = -findMoveNegaMaxAlphaBeta(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
        if score > max_score:
            max_score = score
            if depth == DEPTH:
                next_move = move
        game_state.undoMove()
        if max_score > alpha:
            alpha = max_score
        if alpha >= beta:
            break
    return max_score

def ordermoves(valid_moves):
    
    orderedvalues= np.zeros((len(valid_moves),2))

    for i,move in enumerate(valid_moves):
        orderedvalues[i][0]=(valueofpiece(move.piece_captured) if valueofpiece(move.piece_captured)!=0 else  valueofpiece(move.piece_moved) -valueofpiece(move.piece_moved))
        orderedvalues[i][1]=i

    np.sort(orderedvalues, axis = 0)
    return [
        valid_moves[int(orderedvalues[i][1])]
        for i, move in enumerate(valid_moves)
    ]

def valueofpiece(piece):
    
    if piece=="--" or piece[1]=="K":
        value=0
    if piece[1]=="p":
        value=1
    elif piece[1]=="R":
        value=5
    elif piece[1] in ["N", "B"]:
        value=3
    elif piece[1]=="Q":
        value=9
    return value



def scoreBoard(game_state):
    """
    Score  board. positive score good for white, negative scorec good for black.
    """
    if game_state.checkmate:
        return -CHECKMATE if game_state.white_to_move else CHECKMATE
    elif game_state.stalemate:
        return STALEMATE
    score = 0
    for row in range(len(game_state.board)):
        for col in range(len(game_state.board[row])):
            piece = game_state.board[row][col]
            if piece != "--":
                piece_position_score = 0
                piece_position_score = piece_position_scores[piece][row][col]
                    
                if piece[0] == "w":
                    score += piece_score[piece[1]] + piece_position_score
                if piece[0] == "b":
                    score -= piece_score[piece[1]] + piece_position_score

    return score


def findMove(game_state, valid_moves):
    """
    Picks and returns the best valid move.
    """
    score=0,None
    for i in valid_moves:
        game_state.makeMove(i)
        if score[0]<scoreBoard(game_state):
            score=scoreBoard(game_state),i
        game_state.undoMove()

    return score[1]
