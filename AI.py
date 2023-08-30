from decision_tree import *
from board import *


class AI:
    def __init__(self, board, symbol):
        self.board = [row[:] for row in board]
        self.symbol = symbol
        self.tree = Decision_tree(self.board)

    def get_decision(self):

        best_score = -self.symbol * 999999
        best_move = None
        best_outcome = None

        return Decision_tree.get_best_node_in_layers(self.tree, self.symbol)


    def update_board(self, board):
        self.board = Board.board_copy(board)
        self.tree = Decision_tree(Board.board_copy(board))
