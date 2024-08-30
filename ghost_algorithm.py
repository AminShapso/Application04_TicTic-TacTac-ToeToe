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
    global num_players
    global move_counter
    global player, opponent
    global height, width
    global row_sequence, column_sequence, diagonal_sequence
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


def evaluate_old(board):
    """This is the evaluation function"""
    # Checking for Rows for X or O victory.
    for row in range(height):
        if all([board[row][i] == player for i in range(3)]):
            return 10
        if all([board[row][i] == opponent for i in range(3)]):
            return -10

    # Checking for Columns for X or O victory.
    for col in range(width):
        if all([board[i][col] == player for i in range(3)]):
            return 10
        if all([board[i][col] == opponent for i in range(3)]):
            return -10

    # Checking for Diagonals for X or O victory.
    if all([board[i][i] == player for i in range(3)]):
        return 10
    if all([board[i][i] == opponent for i in range(3)]):
        return -10

    if all([board[i][j] == player for i, j in zip(range(3), reversed(range(3)))]):
        return 10
    if all([board[i][j] == opponent for i, j in zip(range(3), reversed(range(3)))]):
        return -10
    return 0  # Else if none of them have won then return 0


def evaluate_new(board):
    """This is the evaluation function as discussed in the previous article (http://goo.gl/sJgv68)"""
    # Checking for Rows for X or O victory.
    for row in range(height):
        for c in range(width - row_sequence + 1):
            if all([board[row][i + c] == player for i in range(row_sequence)]):
                return 10
            elif all([board[row][i + c] == opponent for i in range(row_sequence)]):
                return -10

    # Checking for Columns for X or O victory.
    for col in range(width):
        for r in range(height - column_sequence + 1):
            if all([board[i + r][col] == player for i in range(column_sequence)]):
                return 10
            elif all([board[i + r][col] == opponent for i in range(column_sequence)]):
                return -10

    # Checking for Diagonals for X or O victory.
    for row, col in zip([0] * (height - 1) + list(range(width)), list(reversed(range(height))) + [0] * (width - 1)):
        for r, c in zip(range(row - diagonal_sequence + 1, row + 1), range(col - diagonal_sequence + 1, col + 1)):
            if 0 <= r <= (height - diagonal_sequence) and 0 <= c <= (width - diagonal_sequence):
                if all([board[r + i][c + i] == player for i in range(diagonal_sequence)]):
                    return 10
                elif all([board[r + i][c + i] == opponent for i in range(diagonal_sequence)]):
                    return -10
    # Check backward diagonal:
    for row, col in zip(list(range(width)) + [width - 1] * (height - 1), [0] * (width - 1) + list(range(height))):
        for r, c in zip(reversed(range(row, row + diagonal_sequence)), range(col - diagonal_sequence + 1, col + 1)):
            if diagonal_sequence - 1 <= r <= height - 1 and 0 <= c <= (width - diagonal_sequence):
                if all([board[r - i][c + i] == player for i in range(diagonal_sequence)]):
                    return 10
                elif all([board[r - i][c + i] == opponent for i in range(diagonal_sequence)]):
                    return -10
    return 0  # Else if none of them have won then return 0


def minimax(board, depth, maximizing_player, max_depth):
    """This is the minimax function. It considers all the possible ways the game can go and returns the value of the board"""
    if max_depth is not None and depth > max_depth:
        return 0
    if new_method:
        score = evaluate_new(board)
    else:
        score = evaluate_old(board)
    if score == 10:  # If Maximizer has won the game return his/her evaluated score
        return score
    if score == -10:  # If Minimizer has won the game return his/her evaluated score
        return score
    if not is_moves_left(board):  # If there are no more moves and no winner then it is a tie
        return 0
    if maximizing_player:
        best = -1000
        for r in range(height):
            for c in range(width):
                if board[r][c] is None:
                    board[r][c] = player
                    best = max(best, minimax(board, depth + 1, not maximizing_player, max_depth))  # Call minimax recursively and choose the maximum value
                    board[r][c] = None  # Undo the move
        return best

    else:  # If this minimizer's move
        best = 1000
        for r in range(height):
            for c in range(width):
                if board[r][c] is None:
                    board[r][c] = opponent
                    best = min(best, minimax(board, depth + 1, not maximizing_player, max_depth))  # Call minimax recursively and choose the minimum value
                    board[r][c] = None  # Undo the move
        return best


def find_best_move(board, max_depth=None):
    best_val = -1000
    best_move = (-1, -1)

    # Traverse all cells, evaluate minimax function for all empty cells. And return the cell with optimal value
    for r in range(height):
        for c in range(width):
            if board[r][c] is None:  # Check if cell is empty
                board[r][c] = player  # Make the move
                move_val = minimax(board, 0, False, max_depth)  # compute evaluation function for this move
                board[r][c] = None  # Undo the move
                if new_method and move_val == 0:
                    best_move = (-1, -1)
                elif move_val > best_val:  # If the value of the current move is more than the best value, then update best
                    best_move = (r, c)
                    best_val = move_val
    return best_move


if __name__ == "__main__":
    best_move = find_best_move(board)
    print("The Optimal Move is :")
    print("ROW:", best_move[0], " COL:", best_move[1])
