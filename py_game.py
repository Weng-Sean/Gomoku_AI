import pygame
from AI import *
from decision_tree_v2 import *
from threading import Thread

pygame.font.init()
pygame.init()
DIMENSION = 15
WIDTH = 700
HEIGHT = 700
ROW_INC = HEIGHT / (DIMENSION + 1)
COL_INC = WIDTH / (DIMENSION + 1)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gomoku")


def draw_grid():
    idx_row = 0
    for row in range(DIMENSION + 1):
        pygame.draw.line(screen, (0, 0, 0), (0, int(idx_row)), (WIDTH, int(idx_row)), 3)
        idx_row += ROW_INC

    idx_col = 0
    for col in range(DIMENSION + 1):
        pygame.draw.line(screen, (0, 0, 0), (int(idx_col), 0), (int(idx_col), HEIGHT), 3)
        idx_col += COL_INC

    for r in range(1, DIMENSION + 1):
        coor = get_coor(r, 0)[2]
        msg2screen(str(r), coor[0], coor[1], (255, 125, 0))
    for c in range(1, DIMENSION + 1):
        coor = get_coor(0, c)[2]
        msg2screen(str(c), coor[0], coor[1], (255, 125, 0))
    draw_board(board_obj)


def get_coor(r, c):
    coor1 = (int(r * ROW_INC), int(c * COL_INC))
    coor2 = (int((r + 1) * ROW_INC), int((c + 1) * COL_INC))
    center = (int((coor1[0] + coor2[0]) / 2), int((coor1[1] + coor2[1]) / 2))
    return coor1, coor2, center


def msg2screen(txt, x, y, color=(0, 0, 0), size=35):
    screen_txt = pygame.font.SysFont(None, size).render(txt, True, color)
    screen.blit(screen_txt, (int(x - size / 6 * len(txt)), int(y - size / 4)))


def get_rc(x, y):
    row = max(1, int(y // ROW_INC))
    row = min(DIMENSION, row)
    col = max(1, int(x // COL_INC))
    col = min(DIMENSION, col)

    return row, col


def highlight(x, y, color=(0, 255, 0)):
    row, col = get_rc(x, y)

    highlight_rc(row, col, color)


def highlight_rc(row, col, color=(0, 255, 0)):
    coordinate = get_coor(row, col)
    y1, x1 = coordinate[0]
    y2, x2 = coordinate[1]
    if row >= 1 and row < DIMENSION + 1 and col >= 1 and col < DIMENSION + 1:
        pygame.draw.line(screen, color, (x1, y1), (x2, y1), 3)
        pygame.draw.line(screen, color, (x2, y2), (x1, y2), 3)
        pygame.draw.line(screen, color, (x1, y1), (x1, y2), 3)
        pygame.draw.line(screen, color, (x2, y2), (x2, y1), 3)


def draw_board(board_obj):
    board = board_obj.board
    for row in range(DIMENSION):
        for col in range(DIMENSION):
            if board[row][col] != 0:
                draw_circle(board[row][col], row + 1, col + 1)


def draw_circle(symbol, row, col, width=0, color=None):
    y, x = get_coor(row, col)[2]
    if not color:
        if symbol > 0:
            color = (0, 0, 0)
        else:
            color = (255, 255, 255)
    pygame.draw.circle(screen, color, (x, y), int(min(ROW_INC, COL_INC) / 2), width)

def AI_turn():
    global last_move, AI_done_thinking, AI_decision
    A = AI(board_obj.board, board_obj.turn)
    AI_decision = A.get_decision()
    AI_done_thinking = True

board_obj = None
run = True
finished = False
main_page = True
player1 = None
player2 = None
players_dic = None
last_move = None
AI_start_thinking = False
AI_done_thinking = False
AI_decision = None

move = 0

while run:
    mouse_x, mouse_y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
    if main_page:
        player1 = None
        player2 = None
        board_obj = Board(DIMENSION)
        last_move = None
        players_dic = None
        finished = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # human vs human
                if 260 < mouse_x < 480 and 140 < mouse_y < 170:
                    player1 = "hm"
                    player2 = "hm"

                # human vs AI
                elif 260 < mouse_x < 480 and 240 < mouse_y < 270:
                    player1 = "hm"
                    player2 = "ai"
                # AI vs human
                elif 260 < mouse_x < 480 and 340 < mouse_y < 370:
                    player1 = "ai"
                    player2 = "hm"
                # AI vs AI
                elif 260 < mouse_x < 480 and 440 < mouse_y < 470:
                    player1 = "ai"
                    player2 = "ai"
        screen.fill((50, 100, 200))
        if 260 < mouse_x < 480 and 140 < mouse_y < 170:
            msg2screen("Human v.s Human", HEIGHT / 2, WIDTH / 2 - 200, size=40)
        else:
            msg2screen("Human v.s Human", HEIGHT / 2, WIDTH / 2 - 200)

        if 260 < mouse_x < 480 and 240 < mouse_y < 270:
            msg2screen("Human v.s AI", HEIGHT / 2, WIDTH / 2 - 100, size=40)
        else:
            msg2screen("Human v.s AI", HEIGHT / 2, WIDTH / 2 - 100)

        if 260 < mouse_x < 480 and 340 < mouse_y < 370:
            msg2screen("AI v.s Human", HEIGHT / 2, WIDTH / 2, size=40)
        else:
            msg2screen("AI v.s Human", HEIGHT / 2, WIDTH / 2)

        if 260 < mouse_x < 480 and 440 < mouse_y < 470:
            msg2screen("AI v.s AI", HEIGHT / 2, WIDTH / 2 + 100, size=40)
        else:
            msg2screen("AI v.s AI", HEIGHT / 2, WIDTH / 2 + 100)

        if player1 and player2:
            players_dic = {1: player1, -1: player2}
            print(players_dic)
            main_page = False

    # exit the main page
    else:

        if not finished:
            winner = board_obj.is_win()
        else:
            winner = None
        # when game is not finished
        if not winner:
            screen.fill((50, 100, 200))
            draw_grid()
            if last_move:
                draw_circle(board_obj.turn, last_move[0], last_move[1], 2, color=(255, 125, 0))

            # check if it's finished and display play again
            if finished:
                if 285 < mouse_x < 424 and 237 < mouse_y < 273:
                    msg2screen("Play again", HEIGHT / 2, WIDTH / 2 - 100, size=40, color=(255, 125, 0))
                else:
                    msg2screen("Play again", HEIGHT / 2, WIDTH / 2 - 100, color=(255, 125, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if players_dic[board_obj.turn] == "hm":
                        row, col = get_rc(mouse_x, mouse_y)

                        if not finished:
                            board_obj.play(row, col)
                            draw_board(board_obj)
                            pygame.display.flip()
                            # draw last move circle
                            last_move = (row, col)
                            draw_circle(board_obj.turn, last_move[0], last_move[1], 2, color=(255, 125, 0))

                            # print out score
                            # Decision_tree.get_score((row - 1, col - 1), board_obj.board)

                            move += 1
                            pygame.image.save(screen, f"last_game/move{move}.png")
                        # check whether play again bottom is clicked
                        else:
                            # play again
                            if 285 < mouse_x < 424 and 237 < mouse_y < 273:
                                main_page = True


            if players_dic[board_obj.turn] == "hm":
                row, col = get_rc(mouse_x, mouse_y)
                draw_circle(board_obj.turn, row, col, 3)
            else:
                highlight(mouse_x, mouse_y)

            if players_dic[board_obj.turn] == "ai":
                if not board_obj.is_win():

                    if not AI_start_thinking:
                        Thread(target=AI_turn).start()
                        AI_start_thinking = True
                    if AI_done_thinking:
                        board_obj.board = AI_decision.board
                        board_obj.turn = -board_obj.turn
                        last_move = (AI_decision.index[0]+1, AI_decision.index[1]+1)
                        AI_start_thinking = False
                        AI_done_thinking = False

                        draw_grid()
                        move += 1
                        pygame.image.save(screen, f"last_game/move{move}.png")






        # when game is finished, show the result
        else:
            screen.fill((50, 100, 200))
            if winner == 1:
                winner_str = "Player 1"
            else:
                winner_str = "Player 2"

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # play again
                    if 285 < mouse_x < 424 and 237 < mouse_y < 273:
                        main_page = True
                    # Go back
                    if 285 < mouse_x < 424 and 337 < mouse_y < 373:
                        finished = True

            msg2screen(winner_str + " won the game!", HEIGHT / 2, WIDTH / 2 - 200)

            if 285 < mouse_x < 424 and 237 < mouse_y < 273:
                msg2screen("Play again", HEIGHT / 2, WIDTH / 2 - 100, size=40)
            else:
                msg2screen("Play again", HEIGHT / 2, WIDTH / 2 - 100)

            if 285 < mouse_x < 424 and 337 < mouse_y < 373:
                msg2screen("Go back", HEIGHT / 2, WIDTH / 2, size=40)
            else:
                msg2screen("Go back", HEIGHT / 2, WIDTH / 2)

    pygame.display.flip()
