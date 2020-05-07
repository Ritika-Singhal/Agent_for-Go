import numpy as np
from Board import Board
MIN = -10000
MAX = 10000
# DEPTH = 4


class MinMax:
    def __init__(self):
        self.DEPTH = 3

    def new_board(self, opp_player, previous, move, num_moves, lib_coeff):
        # current = np.copy(previous)
        current = np.array(previous)
        board = Board(opp_player, previous, current, num_moves, lib_coeff)
        if move is not None:
            board.opponent_move(move)

        return board

    def minimax(self, board, max_player, alpha, beta, depth):
        best_action = None

        if max_player:
            if board.terminate() or depth == self.DEPTH:
                return board.evaluate(), 0
            if depth == 0:
                v = alpha
            else:
                v = MIN
            valid_states = board.valid_states(-1)

            while not valid_states.empty():
                priority, action = valid_states.get()

                if action == "PASS":
                    b = self.new_board(board.opp_player, np.array(board.state), None, board.num_moves + 1, board.lib_coeff)
                else:
                    b = self.new_board(board.opp_player, np.array(board.state), action, board.num_moves + 1, board.lib_coeff)

                value, _ = self.minimax(b, False, alpha, beta, depth + 1)

                if value > v:
                    v = value
                    best_action = action
                if v >= beta:
                    return v, best_action
                if v > alpha:
                    alpha = v

            if best_action is None:
                best_action = "PASS"

            return v, best_action
        else:
            if board.terminate() or depth == self.DEPTH:
                return (-1) * board.evaluate(), 0
            v = MAX
            valid_states = board.valid_states(1)
            while not valid_states.empty():
                priority, action = valid_states.get()

                if action == "PASS":
                    b = self.new_board(board.opp_player, np.array(board.state), None, board.num_moves + 1, board.lib_coeff)
                else:
                    b = self.new_board(board.opp_player, np.array(board.state), action, board.num_moves + 1, board.lib_coeff)

                value, _ = self.minimax(b, True, alpha, beta, depth + 1)
                if value < v:
                    v = value
                    best_action = action
                if v <= alpha:
                    return v, best_action
                if v < beta:
                    beta = v

            if best_action is None:
                best_action = "PASS"

            return v, best_action


