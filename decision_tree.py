from board import Board

class Decision_tree:
    def __init__(self, board, index=(-1, -1)):
        self.board = [row[:] for row in board]
        self.dimension = len(self.board)
        self.win_move = False
        self.best_move = None
        self.next_moves = []
        self.index = index
        self.display_index = (self.index[0] + 1, self.index[1] + 1)
        self.evaluate = 0
        score = self.get_score(self.index, self.board)
        self.evaluate = score

    def expand(self, symbol):
        if self.is_win():
            return False

        RANGE = 1


        is_empty = True
        key_board = Board.board_copy(self.board)
        for row in range(self.dimension):
            for col in range(self.dimension):
                if self.board[row][col] != 0:
                    is_empty = False

                    for r in range(max(0, row - RANGE), min(row + RANGE + 1, self.dimension)):
                        for c in range(max(0, col - RANGE), min(col + RANGE + 1, self.dimension)):
                            key_board[r][c] = "*"
        if is_empty:
            key_board[int(self.dimension / 2)][int(self.dimension / 2)] = "*"

        for row in range(self.dimension):
            for col in range(self.dimension):
                if key_board[row][col] == "*" and self.board[row][col] == 0:
                    board_copy = Board.board_copy(self.board)
                    board_copy[row][col] = symbol
                    tree = Decision_tree(board_copy, (row, col))
                    self.next_moves.append(tree)

    @staticmethod
    def get_best_node_in_layers(tree, symbol):
        best_score = -symbol * 999999
        tree.expand(symbol)
        best_move = tree.next_moves[0]
        def layer2_decision(tree, symbol):
            best = -symbol * 999999
            best_move_ = None
            # return false when game is finished
            tree.expand(symbol)

            for layer1 in tree.next_moves:
                layer2 = layer1.get_best_move(-symbol)
                total = layer2.evaluate + layer1.evaluate
                if total * symbol > best * symbol:
                    best = total
                    best_move_ = layer1
            return best_move_


        for a1 in tree.next_moves:

            if a1.is_win():
                return a1
            a2 = layer2_decision(a1, -symbol)
            if a2.is_win():
                continue
            a2.expand(symbol)
            for a3 in a2.next_moves:
                a4 = a3.get_best_move(-symbol)

                score = a1.evaluate + a2.evaluate + a3.evaluate + a4.evaluate

                if symbol * score > best_score * symbol:
                    best_score = score
                    best_move = a1

        return best_move

    def get_best_move(self, symbol, return_score=False):

        is_empty = True
        key_board = Board.board_copy(self.board)
        for row in range(self.dimension):
            for col in range(self.dimension):
                if self.board[row][col] != 0:
                    is_empty = False

                    for r in range(max(0, row - 1), min(row + 2, self.dimension)):
                        for c in range(max(0, col - 1), min(col + 2, self.dimension)):
                            key_board[r][c] = "*"
        if is_empty:
            key_board[int(self.dimension / 2)][int(self.dimension / 2)] = "*"

        best_score = -symbol * 99999
        best_index = None
        best_board = None

        for row in range(self.dimension):
            for col in range(self.dimension):
                if key_board[row][col] == "*" and self.board[row][col] == 0:
                    board_copy = Board.board_copy(self.board)
                    board_copy[row][col] = symbol
                    score = Decision_tree.get_score((row, col), board_copy)
                    if score * symbol > best_score * symbol:
                        best_score = score
                        best_index = (row, col)
                        best_board = board_copy

        tree = Decision_tree(best_board, best_index)
        self.best_move = tree

        if return_score:
            return best_score
        return tree

    @staticmethod
    def get_score(index, board):

        dimension = len(board)
        row = index[0]
        col = index[1]
        symbol = board[row][col]
        if symbol == 0:
            return 0

        def get_row_score():
            left = col - 1
            left_block = False
            right = col + 1
            right_block = False
            count = 1

            run = False
            if left >= 0:
                run = True
            while run:
                token = board[row][left]
                if token == symbol:
                    count += 1
                elif token == -symbol:
                    left_block = True
                    run = False
                else:
                    left_block = False
                    run = False
                if left >= 0:
                    left -= 1
                else:
                    run = False

            if right < dimension:
                run = True
            while run:
                token = board[row][right]
                if token == symbol:
                    count += 1
                elif token == -symbol:
                    right_block = True
                    run = False
                else:
                    right_block = False
                    run = False
                if right < dimension-1:
                    right += 1
                else:
                    run = False

            score = pow(2, count)

            if count >= 5:
                return 11000
            elif count == 4:
                if not (left_block or right_block):
                    return 10000
                elif not (left_block and right_block):
                    score *= 3
            if count == 3 and not (left_block or right_block):
                score *= 3

            return score

        def get_col_score():
            up = row - 1
            up_block = False
            down = row + 1
            down_block = False
            count = 1

            run = False
            if up >= 0:
                run = True
            while run:
                token = board[up][col]
                if token == symbol:
                    count += 1
                elif token == -symbol:
                    up_block = True
                    run = False
                else:
                    up_block = False
                    run = False
                if up >= 0:
                    up -= 1
                else:
                    run = False

            if down < dimension:
                run = True
            while run:
                token = board[down][col]
                if token == symbol:
                    count += 1
                elif token == -symbol:
                    down_block = True
                    run = False
                else:
                    down_block = False
                    run = False
                if down < dimension-1:
                    down += 1
                else:
                    run = False

            score = pow(2, count)

            if count >= 5:
                return 11000
            elif count == 4:
                if not (up_block or down_block):
                    return 10000
                elif not (up_block and down_block):
                    score *= 3
            if count == 3 and not (up_block or down_block):
                score *= 3

            return score

        def get_pos_score():
            up_right_r = row - 1
            up_right_c = col + 1
            up_right_block = False
            down_left_r = row + 1
            down_left_c = col - 1
            down_left_block = False
            count = 1

            run = False
            if up_right_r >= 0 and up_right_c < dimension:
                run = True
            while run:
                token = board[up_right_r][up_right_c]
                if token == symbol:
                    count += 1
                elif token == -symbol:
                    up_right_block = True
                    run = False
                else:
                    up_right_block = False
                    run = False
                if up_right_r >= 0 and up_right_c < dimension-1:
                    up_right_r -= 1
                    up_right_c += 1
                else:
                    run = False

            if down_left_r < dimension and down_left_c >= 0:
                run = True
            while run:
                token = board[down_left_r][down_left_c]
                if token == symbol:
                    count += 1
                elif token == -symbol:
                    down_left_block = True
                    run = False
                else:
                    down_left_block = False
                    run = False
                if down_left_r < dimension-1 and down_left_c >= 0:
                    down_left_r += 1
                    down_left_c -= 1
                else:
                    run = False

            score = pow(2, count)

            if count >= 5:
                return 11000
            elif count == 4:
                if not (up_right_block or down_left_block):
                    return 10000
                elif not (up_right_block and down_left_block):
                    score *= 3
            if count == 3 and not (up_right_block or down_left_block):
                score *= 3

            return score

        def get_neg_score():
            up_left_r = row - 1
            up_left_c = col - 1
            up_left_block = False
            down_right_r = row + 1
            down_right_c = col + 1
            down_right_block = False
            count = 1

            run = False
            if up_left_r >= 0 and up_left_c > 0:
                run = True
            while run:
                token = board[up_left_r][up_left_c]
                if token == symbol:
                    count += 1
                elif token == -symbol:
                    up_left_block = True
                    run = False
                else:
                    up_left_block = False
                    run = False
                if up_left_r >= 0 and up_left_c > 0:
                    up_left_r -= 1
                    up_left_c -= 1
                else:
                    run = False

            if down_right_r < dimension and down_right_c < dimension:
                run = True
            while run:
                token = board[down_right_r][down_right_c]
                if token == symbol:
                    count += 1
                elif token == -symbol:
                    down_right_block = True
                    run = False
                else:
                    down_right_block = False
                    run = False
                if down_right_r < dimension -1  and down_right_c < dimension-1:
                    down_right_r += 1
                    down_right_c += 1
                else:
                    run = False

            score = pow(2, count)

            if count >= 5:
                return 11000
            elif count == 4:
                if not (up_left_block or down_right_block):
                    return 10000
                elif not (up_left_block and down_right_block):
                    score *= 3
            if count == 3 and not (up_left_block or down_right_block):
                score *= 3

            return score

        row_score = get_row_score()
        col_score = get_col_score()
        pos_score = get_pos_score()
        neg_score = get_neg_score()

        #print(index, row_score, col_score, pos_score, neg_score)

        total_score = symbol * (row_score + col_score + neg_score + pos_score)
        #print(total_score)
        return total_score

    def __str__(self):
        return Board.print_(self.board)

    def is_win(self):
        return Board.result(self.board)

