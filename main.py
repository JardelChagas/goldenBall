import random
import sys
from copy import copy
import numpy as np
import pandas as pd


def initialization(genes, pt, tn):
    population = []
    for i in range(pt * tn):
        x = ""
        for j in range(genes):
            x += str(random.randrange(0, 2))
        population.append(x)
    return population


def population_division(pt, tn, population):
    p = np.zeros((tn, pt), list)
    cont = [0] * tn

    for i in range(tn * pt):
        r = random.randint(0, tn - 1)
        while (cont[r] == pt):
            r = random.randint(0, tn - 1)
        x = population.pop()
        p[r, cont[r]] = x
        cont[r] = cont[r] + 1
    return p


def new_season(tq):
    tq = [0] * len(tq)
    return tq


if __name__ == '__main__':
    tn = int(sys.argv[1])
    pt = int(sys.argv[2])
    genes = int(sys.argv[3])
    tq = [0] * tn
    players = initialization(genes, pt, tn)
    teams = population_division(pt, tn, players)
    print(teams)

# P   = tamanho da população P = Tn*Pt
# Tn  = números de times 40
# Pt  = número dejogadores de cada time 11
# Pij = jogador i no time j
# TQi  = Força do time i
# treino 2 e 3 opt
# python main.py tn pt genes
# treino customizado: 1 ponto; 2 pontos e UOBX
# número de partidas 76
# quando melhorar em 5 temporadas
