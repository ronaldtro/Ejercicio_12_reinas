import random
import time
import operator
import importar
import numpy as np
import matplotlib.pyplot as plt

mutation_probability = 0.2


def random_chromosome(size):
    return importar.abrir(size)


def fitness(chromosome):

    horizontal_collisions = sum(
        [chromosome.count(queen)-1 for queen in chromosome])/2
    diagonal_collisions = 0

    pos = []
    for i in range(len(chromosome)):
        agg = [chromosome[i], i]
        pos.append(agg)
    for i in range(len(chromosome)):
        j = i+1
        while (j < 4):
            if (abs(pos[i][0] - pos[j][0]) == abs(pos[i][1] - pos[j][1])):
                diagonal_collisions += 1
            j += 1
    fit = int(maxFitness - (diagonal_collisions + horizontal_collisions))
    return fit


def probability(chromosome, fitness):
    return fitness(chromosome) / maxFitness


def random_pick(population, probabilities):
    populationWithProbabilty = zip(population, probabilities)
    total = sum(w for c, w in populationWithProbabilty)
    r = random.uniform(0, total)
    upto = 0
    for c, w in zip(population, probabilities):
        if upto + w >= r:
            return c
        upto += w
    assert False, "Shouldn't get here"


def reproduce(x, y):
    n = len(x)
    c = random.randint(0, n - 1)
    return x[0:c] + y[c:n]


def mutate(x):
    n = len(x)
    c = random.randint(0, n - 1)
    m = random.randint(1, n-1)
    x[c] = m
    return x


def genetic_queen(population, fitness):
    new_population = []
    probabilities = [probability(n, fitness) for n in population]

    for i in range(len(population)):
        x = random_pick(population, probabilities)
        y = random_pick(population, probabilities)
        child = reproduce(x, y)
        if random.random() < mutation_probability:
            child = mutate(child)
        new_population.append(child)

    return new_population


def print_chromosome(chrom):
    print("Chromosome = {},  Fitness = {}"
          .format(str(chrom), fitness(chrom)))


def GAnqueens(nq, maxFitness, population):
    # promedioFitness=0.0
    generation = 1
    progreso = []
    progresoPopulation = []
    pp = 0
    higherFitness = 0
    MAXGENERATION = 5000
    start = time.time()

    while not maxFitness in [fitness(chrom) for chrom in population] and generation <= MAXGENERATION:
        population = genetic_queen(population, fitness)
        # print("")
        higherFitness = max([fitness(n) for n in population])
        for n in population:
            pp += fitness(n)

        generation += 1
        progreso.append(higherFitness)
        progresoPopulation.append(pp)
        pp = 0
        # x=0
    if (generation < MAXGENERATION):
        print("Solucionado en la generacion {}!".format(generation-1))
    else:
        print("Se llegó a la máxima iteracion sin obtener una solución")
    end = time.time()
    print("TIEMPO: ", end-start)
    print()

    plt.plot(progreso)
    plt.ylabel('Max Fitness')
    plt.xlabel('Generation')
    plt.show()

    plt.plot(progresoPopulation)
    plt.ylabel('Population Fitness')
    plt.xlabel('Generation')
    plt.show()


if __name__ == "__main__":
    nq = 8
    maxFitness = ((nq*(nq-1))/2)
    population = [random_chromosome(nq) for _ in range(100)]
    for i in range(10):
        print("ITERACION #{}".format(i))
        GAnqueens(nq, maxFitness, population)
