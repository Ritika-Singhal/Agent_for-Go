import numpy as np
from collections import deque
from queue import PriorityQueue
import time


class Board:
    def __init__(self, player, previous_board, current_board, num_moves, lib_coeff):
        self.player = player
        self.previous_board = previous_board
        self.state = current_board
        if self.player == 1:
            self.opp_player = 2
        else:
            self.opp_player = 1

        # self.state_copy = np.copy(current_board)
        self.state_copy = np.array(current_board)
        self.num_moves = num_moves
        self.lib_coeff = lib_coeff

    def point_neighbours(self, position):
        neighbour_class = {0: set(), 1: set(), 2: set()}
        neighbours = [(position[0] + 1, position[1]), (position[0] - 1, position[1]), (position[0], position[1] + 1),
                      (position[0], position[1] - 1)]

        for i in neighbours:
            if 0 <= i[0] < 5 and 0 <= i[1] < 5:
                neighbour_class[self.state[i[0]][i[1]]].add(i)
        return neighbour_class

    def get_positions(self, stone_color):
        x = set()
        for i in range(5):
            for j in range(5):
                if self.state[i][j] == stone_color:
                    x.add((i, j))
        return x

    def capture_stones(self, position, opp_player):
        neighbours = self.point_neighbours(position)[opp_player]
        capture_points = set([])
        for i in neighbours:
            if i in capture_points:
                continue
            points, liberties = self.find_liberties(i, opp_player)
            if len(liberties) == 0:
                capture_points.update(points)
        for i in capture_points:
            self.state[i[0]][i[1]] = 0
        return capture_points

    def my_move(self, position):
        self.state[position[0]][position[1]] = self.player
        self.capture_stones(position, self.opp_player)
        # self.state_copy = np.copy(self.state)
        self.state_copy = np.array(self.state)
        self.num_moves += 1

    def opponent_move(self, position):
        self.state[position[0]][position[1]] = self.opp_player
        self.capture_stones(position, self.player)
        # self.state_copy = np.copy(self.state)
        self.state_copy = np.array(self.state)

    def valid_states(self, order):
        # valid_states = np.where(self.state == 0)
        # valid_states = np.concatenate(([valid_states[0]], [valid_states[1]]), axis=0).T
        valid_states = self.get_positions(0)

        valid_queue = PriorityQueue()
        if np.count_nonzero(self.previous_board) == 0 and np.count_nonzero(self.state) == 0:
            valid_queue.put((0, (2, 2)))
            return valid_queue

        if (self.previous_board == self.state).all():
            if self.eval() > 0:
                valid_queue.put((0, "PASS"))
                return valid_queue

        if len(valid_states) <= 5:
            valid_queue.put((0, "PASS"))

        for i in valid_states:
            is_valid, capture = self.check_validity(i)
            if is_valid:
                points, _ = self.find_liberties(tuple(i), self.player)

                neighbour = self.point_neighbours(tuple(i))

                # self.state[i[0]][i[1]] = self.player
                opp_neigh = neighbour[self.opp_player]
                # capture = self.capture_stones(tuple(i), self.opp_player)

                valid_queue.put((order * (len(points) + 4 * len(capture) +
                                          2 * ((i[0] % 2) + (i[1] % 2)) + 2 * ((i[0] == 2) or (i[1] == 2)) + 2 * (
                                              len(opp_neigh))), tuple(i)))
            # self.state = np.copy(self.state_copy)
            #     self.state = np.array(self.state_copy)

        if valid_queue.empty():
            valid_queue.put((0, "PASS"))

        return valid_queue

    def check_KO(self, move):
        self.state[move[0]][move[1]] = self.player
        captures = self.capture_stones(move, self.opp_player)

        is_KO = False

        if (self.previous_board == self.state).all():
            is_KO = True

        # self.state = np.copy(self.state_copy)
        self.state = np.array(self.state_copy)
        return is_KO, captures

    def check_suicide(self, move):
        neighbours = self.point_neighbours(move)
        if len(neighbours[0]) == 0:
            points = set()
            for i in neighbours[self.player]:
                if i in points:
                    continue
                p, liberties = self.find_liberties(i, self.player)
                points.update(p)
                if len(liberties) >= 2:
                    return False

            points = set()
            for i in neighbours[self.opp_player]:
                if i in points:
                    continue
                p, liberties = self.find_liberties(i, self.opp_player)
                points.update(p)
                if len(liberties) == 1:
                    return False

            return True

        return False

    def find_liberties(self, position, player):
        points = set()
        liberties = set()

        stack = deque()
        stack.append(position)

        while stack:
            p = stack.pop()
            points.add(p)
            neighbours = self.point_neighbours(p)
            liberties.update(neighbours[0])
            for i in neighbours[player]:
                if i not in points and i not in stack:
                    stack.append(i)

        return points, liberties

    def check_validity(self, move):
        # if self.check_suicide(move) or self.check_KO(move):
        if self.check_suicide(move):
            return False, None
        else:
            is_ko, capture = self.check_KO(move)
            if is_ko:
                return False, None
            return True, capture

    def evaluate(self):
        player_1 = np.count_nonzero(self.state == self.player)
        player_2 = np.count_nonzero(self.state == self.opp_player)
        stone_pieces = player_1 - player_2

        my_eyes = 0
        opp_eyes = 0
        # points = np.where(self.state == 0)
        # points = np.concatenate(([points[0]], [points[1]]), axis=0).T
        points = self.get_positions(0)

        for i in points:
            n = self.point_neighbours(tuple(i))
            if len(n[self.opp_player]) == 0 and len(n[0]) == 0:
                my_eyes += 1

            if len(n[self.player]) == 0 and len(n[0]) == 0:
                opp_eyes += 1

        eyes = my_eyes - opp_eyes

        my_point, my_liberties = self.all_liberties(self.player)
        opp_point, opp_liberties = self.all_liberties(self.opp_player)

        liberties = len(my_liberties) - len(opp_liberties)

        my_count_2 = np.count_nonzero(self.state[:, 2] == self.player) + np.count_nonzero(self.state[2] == self.player)
        opp_count_2 = np.count_nonzero(self.state[:, 2] == self.opp_player) + np.count_nonzero(
            self.state[2] == self.opp_player)

        return self.lib_coeff[0] * stone_pieces + 1 * (my_count_2 - opp_count_2) + 2 * eyes + 4 * min(max(liberties,
                self.lib_coeff[1]), 3) + self.lib_coeff[2] * (len(my_point) - len(opp_point))

    def all_liberties(self, player):
        # stones = np.where(self.state == player)
        # stones = np.concatenate(([stones[0]], [stones[1]]), axis=0).T
        stones = self.get_positions(player)

        points = set()
        liberties = set()
        extra = set()

        for i in stones:
            if tuple(i) in extra:
                continue
            ps, ls = self.find_liberties(tuple(i), player)
            extra.update(ps)
            if len(ps) > len(points):
                points = ps
            liberties.update(ls)

        return points, liberties

    def terminate(self):
        if self.num_moves == 24:
            return True
        return False

    def count_stones(self):
        if self.player == 2:
            return 2.5 + np.count_nonzero(self.state == 2)
        else:
            return np.count_nonzero(self.state == 1)

    def eval(self):
        player_1 = np.count_nonzero(self.state == 1)
        player_2 = 2.5 + np.count_nonzero(self.state == 2)

        if self.player == 2:
            return player_2 - player_1
        else:
            return player_1 - player_2
