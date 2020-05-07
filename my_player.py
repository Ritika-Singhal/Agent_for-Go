import numpy as np
import time
from BoardMe import BoardMe
from minimax import *
from minimax_me import *


def run_white_human():
    previous_state = np.zeros((5, 5), dtype=np.int)
    current_state = np.zeros((5, 5), dtype=np.int)
    board_AI = Board(1, previous_state, current_state, 0, (10, -2, 6))
    board_me = Board(2, previous_state, board_AI.state, 0, 3)

    max_moves = 0
    is_pass = 0

    while is_pass != 2 and max_moves < 24:
        board_AI.num_moves = max_moves
        if board_AI.num_moves > 5:
            minmax.DEPTH = 4
        v, move = minmax.minimax(board_AI, True, MIN, MAX, 0)

        if move == "PASS":
            print("AI move: ", move)
            print(board_AI.state)
            board_me.previous_board = np.copy(board_AI.state)
            board_me.state = np.copy(board_AI.state)
            board_me.state_copy = np.copy(board_AI.state)
            is_pass += 1
        else:
            previous_state = np.copy(board_AI.state)
            board_AI.my_move(move)

            print("AI move: ", move)
            print(board_AI.state)

            board_me.previous_board = np.copy(previous_state)
            board_me.state = np.copy(board_AI.state)
            board_me.state_copy = np.copy(board_AI.state)
            is_pass = 0

        max_moves += 1

        if max_moves == 24:
            break

        if is_pass == 2:
            break

        human = input("Enter your move: ")

        if human == "PASS":
            print("AI move: ", human)
            print(board_me.state)
            board_AI.previous_board = np.copy(board_me.state)
            board_AI.state = np.copy(board_me.state)
            board_AI.state_copy = np.copy(board_me.state)
            is_pass += 1
        else:
            human = human.split(",")
            x = int(human[0])
            y = int(human[1])
            previous_state = np.copy(board_me.state)
            board_me.my_move(tuple([x, y]))

            print("AI move: ", human)
            print(board_me.state)

            board_AI.previous_board = np.copy(previous_state)
            board_AI.state = np.copy(board_me.state)
            board_AI.state_copy = np.copy(board_me.state)
            is_pass = 0
        max_moves += 1

    print("AI: ", board_AI.count_stones())
    print("Me: ", board_me.count_stones())


def run_black_human():
    previous_state = np.zeros((5, 5), dtype=np.int)
    current_state = np.zeros((5, 5), dtype=np.int)
    board_AI = Board(2, previous_state, current_state, 0, (15, -3, 10))
    board_me = Board(1, previous_state, board_AI.state, 0, 4)

    max_moves = 0
    is_pass = 0

    while is_pass != 2 and max_moves < 24:
        human = input("Enter your move: ")

        if human == "PASS":
            print("AI move: ", human)
            print(board_me.state)
            board_AI.previous_board = np.copy(board_me.state)
            board_AI.state = np.copy(board_me.state)
            board_AI.state_copy = np.copy(board_me.state)
            is_pass += 1
        else:
            human = human.split(",")
            x = int(human[0])
            y = int(human[1])
            previous_state = np.copy(board_me.state)
            board_me.my_move(tuple([x, y]))

            print("AI move: ", human)
            print(board_me.state)

            board_AI.previous_board = np.copy(previous_state)
            board_AI.state = np.copy(board_me.state)
            board_AI.state_copy = np.copy(board_me.state)
            is_pass = 0
        max_moves += 1

        if max_moves == 24:
            break

        if is_pass == 2:
            break

        board_AI.num_moves = max_moves
        if board_AI.num_moves > 5:
            minmax.DEPTH = 4
        s = time.time()
        v, move = minmax.minimax(board_AI, True, MIN, MAX, 0)
        print(time.time()-s)
        if move == "PASS":
            print("AI move: ", move)
            print(board_AI.state)
            board_me.previous_board = np.copy(board_AI.state)
            board_me.state = np.copy(board_AI.state)
            board_me.state_copy = np.copy(board_AI.state)
            is_pass += 1
        else:
            previous_state = np.copy(board_AI.state)
            board_AI.my_move(move)

            print("AI move: ", move)
            print(board_AI.state)

            board_me.previous_board = np.copy(previous_state)
            board_me.state = np.copy(board_AI.state)
            board_me.state_copy = np.copy(board_AI.state)
            is_pass = 0

        max_moves += 1

    print("AI: ", board_AI.count_stones())
    print("Me: ", board_me.count_stones())


if __name__ == "__main__":
    minmax = MinMax()
    # if human is white
    run_white_human()
    # if human is black
    run_black_human()


################ below is the code for playing 2 AI agents together ##############################


# def read_data():
#     file = open("input.txt", "r")
#     data = file.read().splitlines()
#     file.close()
#
#     player = data[0].strip()
#     previous_state = []
#     current_state = []
#
#     for i in data[1:6]:
#         previous_state.append(list(map(int, (i.strip()))))
#
#     for i in data[6:]:
#         current_state.append(list(map(int, (i.strip()))))
#
#     return player, np.array(previous_state), np.array(current_state)
#
#
# def write_output(result, path="output.txt"):
#     res = ""
#     if result == "PASS":
#         res = "PASS"
#     else:
#         res += str(result[0]) + ',' + str(result[1])
#
#     with open(path, 'w') as f:
#         f.write(res)
#
#
# def read_moves():
#     file = open("moves.txt", "r")
#     data = file.read().splitlines()
#     file.close()
#     moves = int(data[0].strip())
#     return moves
#
#
# def write_moves(moves, path='moves.txt'):
#     res = str(moves)
#     with open(path, 'w') as f:
#         f.write(res)


# def run_black():
#     previous_state = np.zeros((5, 5), dtype=np.int)
#     current_state = np.zeros((5, 5), dtype=np.int)
#
#     board_AI = BoardMe(2, previous_state, current_state, 0, -3)
#
#     board_me = Board(1, np.copy(previous_state), np.copy(board_AI.state), 0, (10, -2, 6))
#
#     max_moves = 0
#     is_pass = 0
#
#     while is_pass != 2 and max_moves < 24:
#         board_me.num_moves = max_moves
#         s = time.time()
#         if board_me.num_moves > 4:
#             minmax.DEPTH = 4
#
#         v, human = minmax.minimax(board_me, True, MIN, MAX, 0)
#         # if v < board_me.evaluate():
#         #     human = "PASS"
#         print(time.time()-s)
#
#         if human == "PASS":
#             print("My move: ", human)
#             print(board_me.state)
#             board_AI.previous_board = np.copy(board_me.state)
#             board_AI.state = np.copy(board_me.state)
#             board_AI.state_copy = np.copy(board_me.state)
#             is_pass += 1
#         else:
#             previous = np.copy(board_me.state)
#             print(human)
#             board_me.my_move(human)
#             print("My move: ", human)
#             print(board_me.state)
#
#             board_AI.previous_board = np.copy(previous)
#             board_AI.state = np.copy(board_me.state)
#             board_AI.state_copy = np.copy(board_me.state)
#             is_pass = 0
#
#         max_moves += 1
#
#         if max_moves == 24:
#             break
#
#         if is_pass == 2:
#             break
#
#         s = time.time()
#         board_AI.num_moves = max_moves
#         if board_AI.num_moves > 5:
#             minmax_me.DEPTH = 4
#         v, move = minmax_me.minimax(board_AI, True, MIN, MAX, 0)
#         print(time.time()-s)
#
#         if move == "PASS":
#             print("AI move: ", move)
#             print(board_AI.state)
#             board_me.previous_3board = np.copy(board_AI.state)
#             board_me.state = np.copy(board_AI.state)
#             board_me.state_copy = np.copy(board_AI.state)
#             is_pass += 1
#         else:
#             previous = np.copy(board_AI.state)
#             board_AI.my_move(move)
#
#             print("AI move: ", move)
#             print(board_AI.state)
#
#             board_me.previous_board = np.copy(previous)
#             board_me.state = np.copy(board_AI.state)
#             board_me.state_copy = np.copy(board_AI.state)
#             is_pass = 0
#
#         max_moves += 1
#
#     print("AI: ", board_AI.count_stones())
#     print("Me: ", board_me.count_stones())
#
#
# def run_white():
#     previous_state = np.zeros((5, 5), dtype=np.int)
#     current_state = np.zeros((5, 5), dtype=np.int)
#
#     board_AI = BoardMe(1, previous_state, current_state, 0, -2)
#
#     board_me = Board(2, np.copy(previous_state), np.copy(board_AI.state), 0, (15, -3, 10))
#
#     max_moves = 0
#     is_pass = 0
#
#     while is_pass != 2 and max_moves < 24:
#         s = time.time()
#         board_AI.num_moves = max_moves
#         if board_AI.num_moves > 5:
#             minmax_me.DEPTH = 4
#         _, human = minmax_me.minimax(board_AI, True, MIN, MAX, 0)
#         print(time.time()-s)
#
#         if human == "PASS":
#             print("AI move: ", human)
#             print(board_AI.state)
#             board_me.previous_board = np.copy(board_AI.state)
#             board_me.state = np.copy(board_AI.state)
#             board_me.state_copy = np.copy(board_AI.state)
#             is_pass += 1
#         else:
#             previous = np.copy(board_AI.state)
#             print(human)
#             board_AI.my_move(human)
#             print("AI move: ", human)
#             print(board_AI.state)
#
#             board_me.previous_board = np.copy(previous)
#             board_me.state = np.copy(board_AI.state)
#             board_me.state_copy = np.copy(board_AI.state)
#             is_pass = 0
#
#         max_moves += 1
#
#         if max_moves == 24:
#             break
#
#         if is_pass == 2:
#             break
#
#         s = time.time()
#         board_me.num_moves = max_moves
#         if board_me.num_moves > 4:
#             minmax.DEPTH = 4
#         v, move = minmax.minimax(board_me, True, MIN, MAX, 0)
#
#         print(time.time()-s)
#
#         if move == "PASS":
#             print("My move: ", move)
#             print(board_me.state)
#             board_AI.previous_board = np.copy(board_me.state)
#             board_AI.state = np.copy(board_me.state)
#             board_AI.state_copy = np.copy(board_me.state)
#             is_pass += 1
#         else:
#             previous = np.copy(board_me.state)
#             board_me.my_move(move)
#
#             print("My move: ", move)
#             print(board_me.state)
#
#             board_AI.previous_board = np.copy(previous)
#             board_AI.state = np.copy(board_me.state)
#             board_AI.state_copy = np.copy(board_me.state)
#             is_pass = 0
#
#         max_moves += 1
#
#     print("AI: ", board_AI.count_stones())
#     print("Me: ", board_me.count_stones())


# if __name__ == "__main__":
#     # previous_state = np.array([[0, 0, 1, 0, 1],
#     # [0, 0, 2, 1, 1],
#     # [0, 0, 0, 0, 2],
#     # [0, 0, 0, 0, 0],
#     # [0, 0, 0, 0, 0]])
#     #
#     # current_state = np.array([[0, 0, 1, 0, 1],
#     # [0, 0, 2, 1, 1],
#     # [0, 0, 0, 0, 2],
#     # [2, 0, 0, 0, 0],
#     # [0, 0, 0, 0, 0]])
#     #
#     # board = Board(1, previous_state,current_state)
#
#     # player, previous_board, current_board = read_data()
#     # s = time.time()
#     # v, move = minimax(board, True, MIN, MAX, 0)
#     # print(v, move)
#     # print(time.time()-s)
#
#     # write_output(move)
#     #
#     # to test with manual player
#     #
#     s = time.time()
#
#     print("Running as Black-------------------")
#     minmax = MinMax()
#     minmax_me = MinMaxMe()
#     run_black()
#
#     print("Running as White-------------------")
#     minmax = MinMax()
#     minmax_me = MinMaxMe()
#     run_white()
#
#     print(time.time()-s)






