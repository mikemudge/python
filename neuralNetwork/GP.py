#!/usr/bin/env python

from NN import NN
import numpy as np

import random

class GP:
    def __init__(self, mutationFunc, tester):
        self.iteration = 0
        self.mutate = mutationFunc
        self.tester = tester

    def iterate(self, generation):
        bestUtility = 100000000
        for bot in generation:
            utility = self.tester.calcUtility(bot)
            if utility < bestUtility:
                best = bot
                bestUtility = utility

        # Make generation from mutations of the best?
        nextgen = []
        nextgen.append(best)
        # Add mutations to nextgen
        for i in range(99):
            # Copy the best.
            n = best.copy()
            # Mutate to try and improve.
            self.mutate(n)
            nextgen.append(n)
        return nextgen

# NN mutation logic.
class NNTester:
    def __init__(self):
        self.testset = [
            [0, 0],
            [0, 1],
            [1, 0],
            [1, 1],
        ]
        self.expectations = [0, 1, 1, 0]

    def calcUtility(self, n):
        results = n.process(self.testset)
        results.shape = (4)
        return np.sum(np.abs(results - self.expectations))

def mutate(n):
    n.bias1 += np.random.rand(n.bias1.shape[0]) - .5
    n.weights1 += np.random.rand(n.weights1.shape[0], n.weights1.shape[1]) - .5
    n.bias2 += np.random.rand(n.bias2.shape[0]) - .5
    n.weights2 += np.random.rand(n.weights2.shape[0], n.weights2.shape[1]) - .5

if __name__ == '__main__':
    hidden = 5
    g = [NN(2, hidden, 1) for i in range(100)]

    tester = NNTester()
    gp = GP(mutate, tester)
    for iteration in range(1000):
        g = gp.iterate(g)

        best = tester.calcUtility(g[0])
        if best < 0.0001:
            break

    # g[0] is the best.
    result = g[0].process(tester.testset)
    result.shape = (4)
    print(result)

