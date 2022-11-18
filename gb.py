"""Genetic Algorithm."""
import random

import numpy

from deap import base
from deap import creator
from deap import tools

import matplotlib.pyplot as plt

from contextlib import contextmanager
from datetime import datetime, timedelta
from functools import reduce
from math import ceil, fabs


@contextmanager
def timeit(file_write=None):
    """Context Manager to check runtime."""
    start_time = datetime.now()
    print(f'Tempo de Inicio (hh:mm:ss.ms) {start_time}', file=file_write)
    yield
    end_time = datetime.now()
    time_elapsed = end_time - start_time
    print(f'Tempo de Termino (hh:mm:ss.ms) {end_time}', file=file_write)
    print(f'Tempo Total (hh:mm:ss.ms) {time_elapsed}', file=file_write)


def dist2pt(x1, y1, x2, y2):
    """."""
    return max(fabs(x2 - x1), fabs(y2 - y1))  # Distancia de Chebyschev


def midPoint(x1, y1, x2, y2):
    """."""
    return (x1 + x2) / 2, (y1 + y2) / 2


def plotar(indiv, f):
    """."""
    individuo = decode(indiv)
    fig1, f1_axes = plt.subplots(ncols=1, nrows=1, constrained_layout=True)
    x1, y1, x, y = [], [], [], []
    colors = ['red', 'gray']
    cutA = 1
    i1 = individuo[0][0]
    a1 = edges[i1] if individuo[1][0] == 0 else edges[i1][::-1]
    deslocamentos = []
    x.append(a1[0][0])
    y.append(a1[0][1])
    x.append(a1[1][0])
    y.append(a1[1][1])
    f1_axes.quiver(x[0], y[0], x[1] - x[0], y[1] - y[0],
                   scale_units='xy', angles='xy', scale=1, color=colors[0])
    f1_axes.annotate(str(cutA), midPoint(*a1[0], *a1[1]))
    cutA += 1
    for i in range(len(individuo[0]) - 1):
        i1 = individuo[0][i]  # aresta atual
        i2 = individuo[0][i + 1 if i + 1 < len(individuo[0]) else 0]  # proxima aresta
        a1 = edges[i1] if individuo[1][i] == 0 else edges[i1][::-1]  # atual
        a2 = edges[i2] if individuo[1][
            i + 1 if i + 1 < len(individuo[0]) else 0] == 0 else edges[i2][::-1]  # proxima
        x1, y1, x, y = [], [], [], []
        if a1[1] != a2[0]:  # se a proxima não comecar onde a primeira termina
            x1.append(a1[1][0])
            y1.append(a1[1][1])
            x1.append(a2[0][0])
            y1.append(a2[0][1])
            deslocamentos.append({
                'pontos': [x1[0], y1[0], x1[1] - x1[0], y1[1] - y1[0]],
                'annot': str(cutA),
                'mid': midPoint(*a1[1], *a2[0])
            })
            cutA += 1
        # plota a proxima
        x.append(a2[0][0])
        y.append(a2[0][1])
        x.append(a2[1][0])
        y.append(a2[1][1])
        f1_axes.annotate(str(cutA), midPoint(*a2[0], *a2[1]))
        f1_axes.quiver(x[0], y[0], x[1] - x[0], y[1] - y[0],
                       scale_units='xy', angles='xy', scale=1, color=colors[0])
        cutA += 1
    for i in deslocamentos:
        f1_axes.annotate(i['annot'], (i['mid'][0] - 3, i['mid'][1]))
        f1_axes.quiver(*i['pontos'], width=.005,
                       scale_units='xy', angles='xy', scale=1, color=colors[1])
    f1_axes.set_xlim(*f1_axes.get_xlim())
    f1_axes.set_ylim(*f1_axes.get_ylim())
    plt.show()
    plt.close()


def genIndividuo(edges):
    """
    Generate Individuo.

    args:
        edges -> edges to cut of grapth

    individuo[0]: order of edges
    individuo[1]: order of cut

    """
    v = [random.randint(0, 1) for i in range(len(edges))]
    random.shuffle(v)
    return random.sample(range(len(edges)), len(edges)), v


def genIndividuoRK(edges):
    """
    Generate Individuo.

    args:
        edges -> edges to cut of grapth

    individuo[0]: order of edges
    individuo[1]: order of cut

    """
    return [random.random() for i in range(len(edges))], [
        random.random() for i in range(len(edges))]


def decode(ind):
    """."""
    return [ind[0].index(i) for i in sorted(ind[0])], [0 if i < 0.5 else 1 for i in ind[1]]


def evalCut(individuo, pi=100 / 6, mi=400):
    """
    Eval Edges Cut.

    args:
        pi -> cutting speed
        mi -> travel speed

    if individuo[1][i] == 0 the cut is in edge order
    else the cut is in reverse edge order

    """
    ind = decode(individuo)
    dist = 0
    i1 = ind[0][0]
    a1 = edges[i1] if ind[1][0] == 0 else edges[i1][::-1]
    if a1 != (0.0, 0.0):
        dist += dist2pt(0.0, 0.0, *a1[0]) / mi
    dist += (dist2pt(*a1[0], *a1[1])) / pi
    for i in range(len(ind[0]) - 1):
        i1 = ind[0][i]
        i2 = ind[0][i + 1 if i + 1 < len(ind[0]) else 0]
        a1 = edges[i1] if ind[1][i] == 0 else edges[i1][::-1]
        a2 = edges[i2] if ind[1][i + 1 if i + 1 < len(
            ind[0]
        ) else 0] == 0 else edges[i2][::-1]
        if a1[1] == a2[0]:
            dist += (dist2pt(*a2[0], *a2[1])) / pi
        else:
            dist += (dist2pt(*a1[1], *a2[0])) / mi + (
                dist2pt(*a2[0], *a2[1])) / pi
    iu = ind[0][-1]
    au = edges[iu] if ind[1][-1] == 0 else edges[iu][::-1]
    if au != (0.0, 0.0):
        dist += dist2pt(*au[1], 0.0, 0.0) / mi
    individuo.fitness.values = (dist, )
    return dist,


def main(Tn=40, Pt=11, temporadas=5, partidadas=76, Pe=0.2, Pm=0.3, pe=0.7, file=None):
    """."""
    # criação dos jogadores/times
    times = [toolbox.population(n=Pt) for i in range(Tn)]

    toolbox.register("mate", crossBRKGA, indpb=pe)

    hof = tools.HallOfFame(1)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    logbook = tools.Logbook()
    logbook.header = "temp", "par", 'min', 'max', "avg", "std"
    gens, inds = [], []

    for temp in range(temporadas):
        # Inicio da temporada
        [list(toolbox.map(toolbox.evaluate, time)) for time in times]

        melhor = numpy.min([numpy.min([i.fitness.values for i in time])
                            for time in times])
        p = stats.compile(
            [min([i for i in time], key=lambda i:i.fitness.values) for time in times])
        logbook.record(temp=temp, par=0, **p)
        gens.append([0, 0])
        inds.append(melhor)
        print(logbook.stream, file=file)
        for jogo in range(partidadas):
            # fase de treinamento

            minf = numpy.min([numpy.min([i.fitness.values for i in time]) for time in times])
            men = False
            try:
                if minf < melhor:
                    men = True
                    melhor = minf
            except Exception:
                print(minf)

            p = stats.compile(
                [min([i for i in time], key=lambda i:i.fitness.values) for time in times])
            logbook.record(temp=temp, par=jogo, **p)
            if not men:
                print(logbook.stream)
            else:
                print(logbook.stream, file=file)
            hof.update(reduce(lambda x, i: x + i,
                              [[i for i in time] for time in times]))
            gens.append([temp, jogo])
            inds.append(minf)
        # Fase de Transferencia
    return times, stats, hof, gens, inds


def crossBRKGA(ind1, ind2, indpb):
    """."""
    return [ind1[i] if random.random() < indpb else ind2[i]
            for i in range(min(len(ind1), len(ind2)))]


files = [
    'instance_01_2pol',
    # 'instance_01_3pol',
    # 'instance_01_4pol',
    # 'instance_01_5pol',
    # 'instance_01_6pol',
    # 'instance_01_7pol',
    # 'instance_01_8pol',
    # 'instance_01_9pol',
    # 'instance_01_10pol',
    # 'instance_01_16pol',
    # 'albano',
    # 'blaz1',
    # 'blaz2',
    # 'blaz3',
    # 'dighe1',
    # 'dighe2',
    # 'fu',
    # 'rco1',
    # 'rco2',
    # 'rco3',
    # 'shapes2',
    # 'shapes4',
    # 'instance_artificial_01_26pol_hole',
    # 'spfc_instance',
    # 'trousers',
]

# toolbox of GA
toolbox = base.Toolbox()
# Class Fitness
creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
# Representation Individual
creator.create("Individual", list, fitness=creator.FitnessMin)
tipo = ['packing', 'separated']
if __name__ == "__main__":
    for t in tipo:
        for f in files:
            file = open(f'instancias/separated/instance_01_2pol.txt').read().strip().split('\n')
            edges = []
            if file:
                n = int(file.pop(0))
                for i in range(len(file)):
                    a = [float(j) for j in file[i].split()]
                    edges.append([(a[0], a[1]), (a[2], a[3])])
            # Generate Individual
            toolbox.register("indices", genIndividuoRK, edges)
            # initializ individual
            toolbox.register(
                "individual",
                tools.initIterate,
                creator.Individual,
                toolbox.indices
            )
            
            # exit(0)
            # Generate Population
            toolbox.register("population", tools.initRepeat, list, toolbox.individual)
            # Objective Function
            toolbox.register("evaluate", evalCut)
            # function to execute map
            toolbox.register("map", map)

            hof = None
            file_write = None
            print("GB:", file=file_write)
            print(file=file_write)
            print(f"Execução {t}/{f}:", file=file_write)
            # print(
            #     f"Parametros: P={k[0]}, Pe={k[1]}, Pm={k[2]}, pe=0.7, Parada=150",
            #     file=file_write
            # )
            iteracao = None
            with timeit(file_write=file_write):
                iteracao = main(file=file_write)
            individuoFinal = decode(iteracao[2][0])
            plotar(individuoFinal, 'iteracao')
            individuoFinal2 = [[edges[i] for i in individuoFinal[0]], individuoFinal[1]]
            print("Individuo:", [[edges[i] for i in individuoFinal[0]], individuoFinal[1]], file=file_write)
            print("Fitness: ", iteracao[2][0].fitness.values[0], file=file_write)


'''

def training_2_opt(instace, teams, sizePayer):
    
    for team in teams:
        for player in team:
            continuar = True
            gene1 = None
            gene2 = None
            x = 1
                      
            if(isinstance(player, list)):
                playerL = np.random.choice(a=[False], size=sizePayer)
                while(continuar):
                    continuar=False
                    for i in range(sizePayer):
                        if(i < sizePayer - x):
                            if(not contem_ponto_em_comum(instace[player[9 + i] - 1], instace[player[10 + i] - 1]) ):
                                if(gene1 == None and not playerL[player[9+i]-1]):
                                    gene1 = player.pop(9 + i)
                                    x = x + 1
                                    i = i -1
                                elif(gene2 == None and not playerL[player[9+i]-1]):
                                    gene2 = player.pop(9 + i)
                                    continuar = True
                                    x = x + 1
                                    colocar_aresta(instace, player, gene1, gene2, len(player))
                                    playerL[ gene1 - 1] = True
                                    playerL[ gene2 - 1] = True
                                    gene1 = None 
                                    gene2 = None
                print(continuar)
                        
    
def remover_aresta():
    return ''

def colocar_aresta(instace, player, gene1, gene2, sizePayer):
    
    for i in range(int((sizePayer / 2) + 1)):
        pontocomum = False
        if(i < sizePayer - 1):
            if(gene1 != None and contem_ponto_em_comum(instace[player[9 + i] - 1], instace[gene1 - 1])):
                player.insert(9 + i, gene1)
                gene1 = None
            elif(gene2 != None and contem_ponto_em_comum(instace[player[9 + i] - 1], instace[gene2 - 1])):
                player.insert(9 + i, gene2)
                gene2 = None
            
            if(gene2 == None and gene1 == None):
                pontocomum = True
                break
    if(not pontocomum):
        print("movimenta para o ponto mais próximo")

'''