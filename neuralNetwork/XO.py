#!/usr/bin/env python

from NN import NN
from GP import GP, mutate
import numpy as np

import math
import random

class RandomBot:
    def playWhere(self, board):
        return math.floor(random.random() * 9)

class XOGame:
    def play(self, p):
        board = np.zeros(18)
        reverseboard = np.zeros(18)

        # Decide who goes first.
        player1 = p
        player2 = RandomBot()

        self.winner = None
        for i in range(5):
            index = player1.playWhere(board)
            board[index] = 1
            reverseboard[9 + index] = 1

            # checkWin
            if self.checkWin(board):
                self.winner = player1
                break

            index = player2.playWhere(reverseboard)

            board[9 + index] = 1
            reverseboard[index] = 1

            if self.checkWin(reverseboard):
                self.winner = player2
                break

        self.board = board
        return self

    def checkWin(self, board):
        for i in range(3):
            if board[i] and board[i + 1] and board[i + 2]:
                return True
            if board[i] and board[3 + i] and board[6 + i]:
                return True
        if board[0] and board[4] and board[8]:
            return True
        if board[2] and board[4] and board[6]:
            return True
        return False

class NNPlayer():
    def __init__(self, n):
        self.n = n

    def playWhere(self, board):
        results = self.n.process(board)
        best = 0
        for i in range(9):
            if board[i] + board[i+9] == 0 and results[i] > results[best]:
                best = i
        return best

class XOGameTester:
    def __init__(self):
        self.game = XOGame()
        pass

    def calcUtility(self, n):
        player = NNPlayer(n)

        # TODO should play games against several opponents to ensure good utility.

        fitness = 0
        for i in range(50):
            result = self.game.play(player)
            if result.winner == player:
                continue
            if result.winner is None:
                fitness +=1
                continue
            # Losing is bad.
            fitness += 5

        return fitness

if __name__ == '__main__':

    hidden = 5
    n = NN(18, hidden, 9)

    game = XOGame()
    game.play(NNPlayer(n))

    game.board.shape = (2, 3, 3)
    print(game.winner)
    print(game.board)

    # Now learn how to play
    g = [NN(18, hidden, 9) for i in range(100)]

    tester = XOGameTester()
    gp = GP(mutate, tester)
    for iteration in range(1000):
        g = gp.iterate(g)

        best = tester.calcUtility(g[0])
        print(iteration, best)

    # g[0] is the best.
    player = NNPlayer(g[0])
    game.play(player)

    game.board.shape = (2, 3, 3)
    print(game.winner)
    print(game.board)
