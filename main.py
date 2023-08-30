# from py_game import *
import time
from decision_tree_v2 import *
from AI import AI

def play(play_round, player_1_computer, player_2_computer):
    X_won = 0
    O_won = 0

    for i in range(play_round):

        dimension = 15
        board_obj = Board(dimension)
        A = AI(board_obj.board, -1)
        A2 = AI(board_obj.board, 1)
        board_obj.print_board()

        winner = False

        while not winner:
            if not player_1_computer:
                is_valid = True
                row, col = input("row, col ").split(",")
                try:
                    row = int(row)
                    col = int(col)
                    if row > dimension or row < 1 or col > dimension or col < 1:
                        is_valid = False

                    elif board_obj.board[row - 1][col - 1] != 0:
                        is_valid = False


                except:
                    is_valid = False

                while not is_valid:
                    print("Invalid input, please try again")
                    row, col = input("row, col ").split(",")
                    try:
                        row = int(row)
                        col = int(col)
                        if row > dimension or row < 0 or col > dimension or col < 0:
                            is_valid = False
                        elif board_obj.board[row - 1][col - 1] != 0:
                            is_valid = False
                        else:
                            is_valid = True
                    except:
                        is_valid = False

                # record_obj.log(1, board_obj.hash((row-1,col-1)), (row-1, col-1))
                board_obj.play(row, col)

                board_obj.print_board()
                score = Decision_tree(board_obj.board).evaluate
                if score < 0:
                    print("O score", abs(score))
                else:
                    print("X score", abs(score))
                winner = board_obj.is_win()

            else:
                a = time.time()
                A2.update_board(board_obj.board)
                decision = A2.get_decision()
                if decision == None:
                    print("yield!")
                    break
                board_obj.board = decision.board

                board_obj.print_board()
                if board_obj.turn == -1:
                    print("O Movement ", decision.display_index)
                else:
                    print("X Movement ", decision.display_index)
                score = Decision_tree(board_obj.board).evaluate
                if score < 0:
                    print("O score", abs(score))
                else:
                    print("X score", abs(score))
                print("time used", time.time() - a)

                winner = board_obj.is_win()
                # print("win/lose", iterator.evaluate(board_obj.turn))
                board_obj.turn = -board_obj.turn

            if winner:
                break

            if not player_2_computer:
                is_valid = True
                row, col = input("row, col ").split(",")
                try:
                    row = int(row)
                    col = int(col)
                    if row > dimension or row < 1 or col > dimension or col < 1:
                        is_valid = False

                    elif board_obj.board[row - 1][col - 1] != 0:
                        is_valid = False


                except:
                    is_valid = False

                while not is_valid:
                    print("Invalid input, please try again")
                    row, col = input("row, col ").split(",")
                    try:
                        row = int(row)
                        col = int(col)
                        if row > dimension or row < 0 or col > dimension or col < 0:
                            is_valid = False
                        elif board_obj.board[row - 1][col - 1] != 0:
                            is_valid = False
                        else:
                            is_valid = True
                    except:
                        is_valid = False

                # record_obj.log(-1, board_obj.hash((row-1,col-1)), (row-1, col-1))

                board_obj.play(row, col)

                board_obj.print_board()
                score = Decision_tree(board_obj.board).evaluate
                if score < 0:
                    print("O score", abs(score))
                else:
                    print("X score", abs(score))
                winner = board_obj.is_win()

            else:
                a = time.time()
                A.update_board(board_obj.board)
                decision = A.get_decision()
                if decision == None:
                    print("yield!")
                    break
                board_obj.board = decision.board

                board_obj.print_board()
                if board_obj.turn == -1:
                    print("O Movement ", decision.display_index)
                else:
                    print("X Movement ", decision.display_index)
                score = Decision_tree(board_obj.board).evaluate
                if score < 0:
                    print("O score", abs(score))
                else:
                    print("X score", abs(score))
                print("time used", time.time() - a)

                winner = board_obj.is_win()
                # print("win/lose", iterator.evaluate(board_obj.turn))
                board_obj.turn = -board_obj.turn

        print("Round", i + 1)
        if winner == -1:
            print("O won")
            O_won += 1
        elif winner == 1:
            print("X won")
            X_won += 1
        print("X won", X_won)
        print("O won", O_won)

    print("result")
    print("X won", X_won)
    print("O won", O_won)


play(1, False, True)