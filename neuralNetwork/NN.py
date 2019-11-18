#!/usr/bin/env python

import numpy as np


class NN:
    def __init__(self, inputs, hiddens, outputs):
        self.bias1 = np.random.rand(hiddens) - .5
        self.weights1 = np.random.rand(inputs, hiddens) - .5

        self.bias2 = np.random.rand(outputs) - .5
        self.weights2 = np.random.rand(hiddens, outputs) - .5

    def process(self, inputs):
        hidden = self.sigmoid(np.dot(inputs, self.weights1) + self.bias1)
        return self.sigmoid(np.dot(hidden, self.weights2) + self.bias2)

    def sigmoid(self, layer):
        return 1 / (1 + np.exp(-layer))

    def copy(self):
        n = NN(0, 0, 0)
        n.bias1 = self.bias1.copy()
        n.weights1 = self.weights1.copy()
        n.bias2 = self.bias2.copy()
        n.weights2 = self.weights2.copy()
        return n


if __name__ == '__main__':
    n = NN(2, 5, 1)

    # OR
    n.bias1[0] = -50
    n.weights1[0][0] = 100
    n.weights1[1][0] = 100

    # NAND
    n.bias1[1] = 150
    n.weights1[0][1] = -100
    n.weights1[1][1] = -100

    # AND.
    n.bias2[0] = -150
    n.weights2[0] = 100
    n.weights2[1] = 100

    print(n.process([0, 0]))
    print(n.process([0, 1]))
    print(n.process([1, 0]))
    print(n.process([1, 1]))
