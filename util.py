import matplotlib.pyplot as plt
import numpy as np


def get_initial_solution(predetermined=False, addValue=0):
    with open('reinas8.txt', 'r') as f:
        initial_solution = []

        for row in f.readlines():
            row = [int(x.replace('\n', '')) for x in row.split(',')]
            if (predetermined):
                initial_solution.append(-1)
            else:
                if (sum(row) > 0):
                    initial_solution.append(row.index(1) + addValue)
                else:
                    initial_solution.append(0 + addValue)

        return initial_solution


def draw_convergence(costos):
    plt.rcParams["figure.autolayout"] = True
    plt.plot(costos)
    plt.ylabel('Costo total')
    plt.xlabel('Iteraciones')
    plt.show()
