"""
Tic Tac Toe Player
"""

import math
from operator import itemgetter


X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    if x_count == o_count:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    action_set = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                action_set.add((i, j))
    return action_set


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    i, j = action
    if board[i][j] is not EMPTY:
        raise Exception("Invalid.")
    updated_board = [row[:] for row in board]
    updated_board[i][j] = player(board)
    return updated_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    #checking for occurrences of X and O
    for row in board:
        if all(cell == X for cell in row):
            return X
        elif all(cell == O for cell in row):
            return O
    #check the columns
    for col in range(3):
        if all(board[row][col] == X for row in range(3)):
            return X
        elif all(board[row][col] == O for row in range(3)):
            return O
    #check diagonals
    if all(board[i][i] == X for i in range(3)) or all(board[i][2-i] ==
                                                      X for i in range(3)):
        return X
    elif all(board[i][i] == O for i in range(3)) or all(board[i][2-i] ==
                                                        O for i in range(3)):
        return O
    #no winner yet
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None:
        return True
    for row in board:
        if EMPTY in row:
            return False
    """
    This last return True means that there's a tie.
    """
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0

#board == state from pseudocode

def max_value(board):
    v = -math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = max(v, min_value(result(board, action)))
    return v


def min_value(board):
    v = math.inf
    if terminal(board):
        return utility(board)
    for action in actions(board):
        v = min(v, max_value(result(board, action)))
    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    elif player(board) == X:
        plays = []

        #consider - loop over all possible actions
        for action in actions(board):
            #add our action to the plays list. this is a tuple with the min_value and the action that
            #results to to that value
            plays.append([min_value(result(board, action)), action])
        return plays[::-1][0][1]

    elif player(board) == O:
        plays = []

        for action in actions(board):
            plays.append([max_value(result(board, action)), action])
        return sorted(plays, key=itemgetter(0))[0][1]
