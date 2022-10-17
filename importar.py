import pandas as pd
import numpy as np
archivo = './reinas8.txt'


def abrir(n):

    hoja = "N=" + str(n)
    tablero = pd.read_csv(archivo, header=None)
    tablero = tablero.to_numpy()
    pos = [0]*n
    for i, v in np.ndenumerate(tablero):
        lis = list(i)
        if (v == 'x' or v == 'X'):
            pos[lis[1]] = lis[0]

    return pos


def generararbol(vector, tam):
    grafo = []
    ls = list()
    dic = {}
    i = 0
    aux = tolist(toString(map(str, vector)))
    aux1 = list()
    grafo = generararistas(tolist(aux), tam, i, ls)
    dic[toString(map(str, vector))] = grafo
    print('aux1:', aux1)
    i += 1

    return dic


def toString(ls):
    ls = ''.join(ls)
    return ls


def tolist(st):
    st = map(int, st)
    st = list(st)
    print(st)
    return st


def generararistas(vec, tam, pos, ls):

    j = vec[pos]+1
    k = vec[pos]-1
    while j < tam:
        vec[pos*2+1] = j
        ls.append(toString(map(str, vec)))
        j += 1

    vec[pos] = k+1
    j = k+1

    while (k >= 0):
        vec[pos] = k
        ls.append(toString(map(str, vec)))
        k -= 1
    vec[pos] = j
    return ls


if (__name__ == "__main__"):
    n = 8
    print(generararbol(abrir(n), n))
    print(generararbol(abrir(n*2), n*2))
