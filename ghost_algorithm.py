"""This code is contributed by divyesh072019
Python3 program to find the next optimal move for a player"""
import copy

new_method = False
player, opponent = 1, 0
height, width = 3, 3
row_sequence, column_sequence, diagonal_sequence = 3, 3, 3
board = [
    [0, 1, 0],
    [1, 1, 0],
    [None, None, None]
]


def initilaize(grid_height, grid_width, row_sequence_in, column_sequence_in, diagonal_sequence_in):
    global player, opponent
    global height, width
    global row_sequence, column_sequence, diagonal_sequence
    global board
    height = grid_height
    width = grid_width
    row_sequence = row_sequence_in
    column_sequence = column_sequence_in
    diagonal_sequence = diagonal_sequence_in


def is_moves_left(board):
    """This function returns true if there are moves remaining on the board. It returns false if there are no moves left to play"""
    for r in range(height):
        for c in range(width):
            if board[r][c] is None:
                return True
    return False


def evaluate_old(b):
    """This is the evaluation function as discussed in the previous article (http://goo.gl/sJgv68)"""
    # Checking for Rows for X or O victory.
    for row in range(height):
        if b[row][0] == b[row][1] and b[row][1] == b[row][2]:
            if b[row][0] == player:
                return 10
            elif b[row][0] == opponent:
                return -10

    # Checking for Columns for X or O victory.
    for col in range(width):
        if b[0][col] == b[1][col] and b[1][col] == b[2][col]:
            if b[0][col] == player:
                return 10
            elif b[0][col] == opponent:
                return -10

    # Checking for Diagonals for X or O victory.
    if b[0][0] == b[1][1] and b[1][1] == b[2][2]:
        if b[0][0] == player:
            return 10
        elif b[0][0] == opponent:
            return -10

    if b[0][2] == b[1][1] and b[1][1] == b[2][0]:
        if b[0][2] == player:
            return 10
        elif b[0][2] == opponent:
            return -10

    # Else if none of them have won then return 0
    return 0


def evaluate_new(b):
    """This is the evaluation function as discussed in the previous article (http://goo.gl/sJgv68)"""
    # Checking for Rows for X or O victory.
    for row in range(height):
        for c in range(width - row_sequence + 1):
            if all([b[row][i + c] == player for i in range(row_sequence)]):
                return 10
            elif all([b[row][i + c] == opponent for i in range(row_sequence)]):
                return -10

    # Checking for Columns for X or O victory.
    for col in range(width):
        for r in range(height - column_sequence + 1):
            if all([b[i + r][col] == player for i in range(column_sequence)]):
                return 10
            elif all([b[i + r][col] == opponent for i in range(column_sequence)]):
                return -10

    # Checking for Diagonals for X or O victory.
    for row, col in zip([0] * (height - 1) + list(range(width)), list(reversed(range(height))) + [0] * (width - 1)):
        for r, c in zip(range(row - diagonal_sequence + 1, row + 1), range(col - diagonal_sequence + 1, col + 1)):
            if 0 <= r <= (height - diagonal_sequence) and 0 <= c <= (width - diagonal_sequence):
                if all([b[r + i][c + i] == player for i in range(diagonal_sequence)]):
                    return 10
                elif all([b[r + i][c + i] == opponent for i in range(diagonal_sequence)]):
                    return -10
    # Check backward diagonal:
    for row, col in zip(list(range(width)) + [width - 1] * (height - 1), [0] * (width - 1) + list(range(height))):
        for r, c in zip(reversed(range(row, row + diagonal_sequence)), range(col - diagonal_sequence + 1, col + 1)):
            if diagonal_sequence - 1 <= r <= height - 1 and 0 <= c <= (width - diagonal_sequence):
                if all([b[r - i][c + i] == player for i in range(diagonal_sequence)]):
                    return 10
                elif all([b[r - i][c + i] == opponent for i in range(diagonal_sequence)]):
                    return -10

    # Else if none of them have won then return 0
    return 0


def minimax(board, depth, is_max):
    """This is the minimax function. It considers all the possible ways the game can go and returns the value of the board"""
    if new_method:
        score = evaluate_new(board)
    else:
        score = evaluate_old(board)

    # If Maximizer has won the game return his/her
    # evaluated score
    if score == 10:
        return score

    # If Minimizer has won the game return his/her
    # evaluated score
    if score == -10:
        return score

    # If there are no more moves and no winner then
    # it is a tie
    if not is_moves_left(board):
        return 0

    # If this maximizer's move
    if is_max:
        best = -1000

        # Traverse all cells
        for r in range(height):
            for c in range(width):

                # Check if cell is empty
                if board[r][c] is None:
                    # Make the move
                    board[r][c] = player

                    # Call minimax recursively and choose
                    # the maximum value
                    best = max(best, minimax(board, depth + 1, not is_max))

                    # Undo the move
                    board[r][c] = None
        return best

    # If this minimizer's move
    else:
        best = 1000

        # Traverse all cells
        for r in range(height):
            for c in range(width):

                # Check if cell is empty
                if board[r][c] is None:
                    # Make the move
                    board[r][c] = opponent

                    # Call minimax recursively and choose
                    # the minimum value
                    best = min(best, minimax(board, depth + 1, not is_max))

                    # Undo the move
                    board[r][c] = None
        return best
    # This will return the best possible move for the player


def find_best_move(board):
    print(f'{new_method = }')
    best_val = -1000
    best_move = (-1, -1)

    # Traverse all cells, evaluate minimax function for
    # all empty cells. And return the cell with optimal
    # value.
    for r in range(height):
        for c in range(width):

            # Check if cell is empty
            if board[r][c] is None:

                # Make the move
                board[r][c] = player

                # compute evaluation function for this
                # move.
                move_val = minimax(board, 0, False)

                # Undo the move
                board[r][c] = None

                # If the value of the current move is
                # more than the best value, then update
                # best/
                if move_val > best_val:
                    best_move = (r, c)
                    best_val = move_val
    return best_move


if __name__ == "__main__":
    best_move = find_best_move(board)
    print("The Optimal Move is :")
    print("ROW:", best_move[0], " COL:", best_move[1])
