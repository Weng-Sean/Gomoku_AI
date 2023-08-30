class Board:
    def __init__(self, dimension):
        self.dimension = dimension
        self.board = [[0 for i in range(self.dimension)] for i in range(self.dimension)]
        self.turn = 1

    def print_board(self):
        return Board.print_(self.board)

    @staticmethod
    def print_(board):
        string = ""
        row_count = 1

        col_str = "   "
        for col in range(len(board)):
            if col + 1 < 10:
                col_str += str(col + 1) + "   "
            else:
                col_str += str(col + 1) + "  "
        print(col_str)
        string += col_str + "\n"

        for row in board:
            if row_count < 10:
                row_str = f"{row_count} |"
            else:
                row_str = f"{row_count}|"
            for col in row:
                if col == 0:
                    row_str += "   |"
                elif col == 1:
                    row_str += " X" + " |"
                else:
                    row_str += " O" + " |"
            row_count += 1
            print(row_str)
            string += row_str + "\n"
            print("-" * (len(board) * 4 + 2))
            string += "-" * (len(board) * 4 + 2) + "\n"
        return string

    def play(self, row, col):
        if row <= self.dimension and col <= self.dimension:
            if self.board[row - 1][col - 1] == 0:
                self.board[row - 1][col - 1] = self.turn
                self.turn = - self.turn
            else:
                print("Invalid move")
            # winner = self.is_win()
            # if winner == 1:
            #     print(f"Congratulation, X won!")
            # elif winner == -1:
            #     print(f"Congratulation, O won!")
        else:
            print("Invalid index")

    def is_win(self):
        return Board.result(self.board)

    @staticmethod
    def result(board):
        dimension = len(board)
        for row in board:
            current_element = 0
            count = 0
            for col in row:
                if col != 0:
                    if col != current_element:
                        current_element = col
                        count = 1
                    else:
                        count += 1
                else:
                    current_element = 0
                    count = 0
                if count == 5:
                    return col

        for col in range(dimension):
            current_element = 0
            count = 0
            for row in range(dimension):
                element = board[row][col]
                if element != 0:
                    if element != current_element:
                        current_element = element
                        count = 1
                    else:
                        count += 1
                else:
                    current_element = 0
                    count = 0
                if count == 5:
                    return element

        for idx1 in range(dimension):
            for idx2 in range(dimension):
                if board[idx1][idx2] == 0:
                    continue
                symbol = board[idx1][idx2]
                for i in range(5):
                    if idx1 + i < dimension and idx2 + i < dimension:
                        if board[idx1 + i][idx2 + i] != symbol:
                            break
                        if i == 4:
                            return symbol

        for idx1 in range(dimension):
            for idx2 in range(dimension):
                if board[idx1][idx2] == 0:
                    continue
                symbol = board[idx1][idx2]
                for i in range(5):
                    if idx1 + i < dimension and idx2 - i >= 0:
                        if board[idx1 + i][idx2 - i] != symbol:
                            break
                        if i == 4:
                            return symbol
        return False

    @staticmethod
    def board_copy(board):
        return [row[:] for row in board]

    @staticmethod
    def is_finished_with_index(board, index):
        if index == (-1, -1):
            return False
        dimension = len(board)

        row_count = 1
        col_count = 1
        pos_count = 1
        neg_count = 1
        row, col = index
        row_copy, col_copy = index
        symbol = board[row][col]

        score = 0

        # check row
        while row_copy > 0 and board[row_copy - 1][col] == symbol:
            row_count += 1
            row_copy -= 1
        row_copy = index[0]

        while row_copy + 1 < dimension and board[row_copy + 1][col] == symbol:
            row_count += 1
            row_copy += 1
        row_copy = index[0]

        if row_count >= 5:
            return True

        # check col
        while col_copy > 0 and board[row][col_copy - 1] == symbol:
            col_count += 1
            col_copy -= 1
        col_copy = index[1]

        while col_copy + 1 < dimension and board[row][col_copy + 1] == symbol:
            col_count += 1
            col_copy += 1
        col_copy = index[1]

        if col_count >= 5:
            return True

        # check pos
        while col_copy + 1 < dimension and row_copy > 0 and board[row_copy][col_copy + 1] == symbol:
            pos_count += 1
            col_copy += 1
            row_copy -= 1
        row_copy, col_copy = index

        while col_copy > 0 and row_copy + 1 < dimension and board[row_copy + 1][col_copy] == symbol:
            pos_count += 1
            col_copy -= 1
            row_copy += 1
        row_copy, col_copy = index

        if pos_count >= 5:
            return True

        # check neg
        while col_copy > 0 and row_copy > 0 and board[row_copy - 1][col_copy - 1] == symbol:
            neg_count += 1
            col_copy -= 1
            row_copy -= 1
        row_copy, col_copy = index

        while col_copy + 1 < dimension and row_copy + 1 < dimension and board[row_copy + 1][col_copy + 1] == symbol:
            neg_count += 1
            col_copy += 1
            row_copy += 1
        row_copy, col_copy = index

        if neg_count >= 5:
            return True

        return False

    def __str__(self):
        return self.print_board()

    @staticmethod
    def hash_str(board, index):

        row = index[0]
        col = index[1]
        hash_str = ""

        # 9 * 9 square
        for i in range(row - 4, row + 5):
            for j in range(col - 4, col + 5):
                try:
                    hash_str += str(board[i][j])
                except Exception as e:
                    hash_str += "*"
        return hash_str

    def hash(self, index):
        return self.hash_str(self.board, index)
