import sys
from collections import deque
import numpy as np
import random
import math
import time
from util import *

class Node:
    def __init__(self, state, father=None, accion=None, pathCost=0):
        self.state = state
        self.father = father
        self.accion = accion
        self.pathCost = pathCost
        self.depth = 0
        if father:
            self.depth = father.depth + 1

    def expand(self, issue):
        return [self.getNodeChild(issue, action)
                for action in issue.actions(self.state)]

    def getNodeChild(self, issue, action):
        state_next = issue.position_queen(self.state, action)
        next_node = Node(state_next, self, action)
        return next_node

class ProblemaReina:

    def __init__(self):
        self.initial = get_initial_solution(True)
        self.N = len(self.initial)

    def actions(self, state):
        if state[-1] != -1:
            return []
        else:
            col = state.index(-1)
            return [row for row in range(self.N)
                    if not self.isContra(state, row, col)]

    def position_queen(self, state, row):
        col = state.index(-1)
        new = list(state[:])
        new[col] = row
        return list(new)

    def isContra(self, state, row, col):
        return any(self.attack_queen(row, col, state[c], c)
                   for c in range(col))

    def attack_queen(self, row1, col1, row2, col2):
        return (row1 == row2 or
                col1 == col2 or
                row1 - col1 == row2 - col2 or
                row1 + col1 == row2 + col2)

    def value(self, node):
        ataquesCantidad = 0
        for (f1, c1) in enumerate(node.state):
            for (f2, c2) in enumerate(node.state):
                if (f1, c1) != (f2, c2):
                    ataquesCantidad += self.attack_queen(f1, c1, f2, c2)

        return ataquesCantidad

def to_cool(t, k=20, lam=0.005, limit=1000):
    return (k * math.exp(-lam * t) if t < limit else 0)


def simulated_cooling(issue):
    nodoActual = Node(issue.initial)
    costs = []
    i = 0
    while i < 1000000:
        t = to_cool(i)
        if (t == 0 or -1 not in nodoActual.state):
            return [nodoActual.state, costs]
        if (nodoActual.expand(issue) != []):
            n = random.choice(nodoActual.expand(issue))
            deltaE = issue.value(n) - issue.value(nodoActual)
            costs.append(issue.value(n))
            if (not (deltaE > 0 or math.exp(deltaE // t) > 0.5)):
                nodoActual = n
        else:
            nodoActual = Node(issue.initial)
            i =- 1
        i += 1

if __name__ == "__main__":
    inicio = time.time()
    queen_p = ProblemaReina()
    path, costs = simulated_cooling(queen_p)

    for i in range(queen_p.N):
        for j in range(queen_p.N):
            if path[i] == j:
                print('R', end='')
            else:
                print('-', end='')
            print(" ", end='')
        print()
    fin = time.time()
    total = len(costs)
    mayor = 0
    for i in range(len(costs)):
        if costs[i] > mayor:
            mayor = costs[i]
    print(f'Mejor costo: {costs[-1]}')
    print(f'Mayor costo: {mayor}')
    print(f'Cantidad operaciones: {total}')
    print(fin-inicio)
    draw_convergence(costs)
