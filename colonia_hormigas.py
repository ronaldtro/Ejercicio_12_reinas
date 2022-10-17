
import numpy as np
import os
import numpy as np
import time
from util import *

class ACO(object):
    def __init__(self, hormigas, iteraciones, rho, alpha=1, beta=1, semilla=None):
        self.hormigas = hormigas
        self.iteraciones = iteraciones
        self.rho = rho
        self.alpha = alpha
        self.beta = beta
        self.estadosLocales = np.random.RandomState(semilla)
        self.costos = []
        self.solucionInicial = get_initial_solution()
        self.dimension = len(self.solucionInicial)
        self.feromona = np.ones((self.dimension, self.dimension)) / self.dimension

    def resolver(self):
        
        mejorPosicion = None
        mejorCamino = ("TBD", np.inf)
        
        for i in range(self.iteraciones):
            contradicciones = np.zeros((self.hormigas, self.dimension))
            caminos = self.construirColonia(contradicciones)
            self.depositarFeromonas(caminos, contradicciones)
            mejorPosicion = min(caminos, key=lambda x: x[1])
            if mejorPosicion[1] < mejorCamino[1]:
                mejorCamino = mejorPosicion
            self.feromona *= self.rho
        
        return mejorCamino
        

    def depositarFeromonas(self, caminos, contradicciones):
        currPath = 0

        for camino, fitVal in caminos:
            for movimiento in range(self.dimension):
                self.feromona[camino[movimiento]][movimiento] += 1.0 / (contradicciones[currPath][movimiento] + 1)**(self.dimension/2)
            currPath += 1

    def evaluarCamino(self, camino, contradicciones):
        inicio = time.time()
        res = 0
        for i in range(len(camino)):
            if contradicciones[i] != 0:
                res += 1

        self.costos.append(res)
        if res == 0:
            for i in range(self.dimension):
                for j in range(self.dimension):
                    if camino[i] == j:
                        print('R', end='')
                    else:
                        print('-', end='')
                    print(" ", end='')
                print()
            total = len(self.costos)
            mayor = 0
            for i in range(len(self.costos)):
                if self.costos[i] > mayor:
                    mayor = self.costos[i]
            fin = time.time()
            print(f'Mejor costo: {self.costos[-1]}')
            print(f'Mayor costo: {mayor}')
            print(f'Cantidad operaciones: {total}')
            print(fin-inicio)
            draw_convergence(self.costos)
            
            exit(0)


        return res

    def construirSolucion(self, hormiga, contradicciones):
        camino = []
        for i in range(self.dimension):
            camino = self.obtenerSiguienteMovimiento(self.feromona[:][i], camino, hormiga, contradicciones)
        return camino, self.evaluarCamino(camino, contradicciones[hormiga])

    def construirColonia(self, contradicciones):
        caminos = []
        for i in range(self.hormigas):
            camino, valor = self.construirSolucion(i, contradicciones)
            caminos.append((camino, valor))
        return caminos

    def obtenerSiguienteMovimiento(self, feromona, camino, hormiga,contradicciones):
        columnaContradiccion = self.obtenerContradicciones(camino)
        fila = feromona ** self.alpha * ((1.0 / (columnaContradiccion+1)) ** self.beta)
        dimensiones = range(self.dimension)
        movimiento = self.estadosLocales.choice(dimensiones, 1, p=(fila / fila.sum()))[0]
        camino.append(movimiento)
        if columnaContradiccion[movimiento] != 0:
            contradicciones[hormiga][len(camino)-1] += 1
        for j in range((len(camino)-1)):
            if camino[j] == movimiento:
                contradicciones[hormiga][j] += 1
            if camino[j] + j == len(camino) - 1 + movimiento:
                contradicciones[hormiga][j] += 1
            if camino[j] - j == movimiento - (len(camino) - 1):
                contradicciones[hormiga][j] += 1

        return camino

    def obtenerContradicciones(self, camino):
        columnaContradiccion = np.zeros(self.dimension)
        curCol = len(camino)
        for i in range(self.dimension):
            for j in range(len(camino)):
                if camino[j] == i or curCol - i == j - camino[j] or curCol + i == j + camino[j]:
                    columnaContradiccion[i] += 1
        return columnaContradiccion

if __name__ == "__main__":
    iteraciones = 500
    hormigas = 200
    aco = ACO(hormigas, iteraciones, rho=0.95, alpha=1, beta=10)
    aco.resolver()
    
    
    


