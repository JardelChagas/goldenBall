#from cgitb import reset
#import copy
#from this import s
from numpy.random import default_rng
#import matplotlib.pyplot as plt
#import numpy as np
import random
from math import fabs
#from py2opt.routefinder import RouteFinder
import time

def creation_players(instace, size):
    
    rng = default_rng()
    playerR = rng.choice(size, size=size, replace=False).tolist()
    
    for x in range(len(playerR)):
        playerR[x] = playerR[x] + 1

    playerL = [random.randint(0, 1) for i in range(size)]
     

    player = [-1, playerL, playerR]
    player[0] = score_relax(instace, player)
    
    return player

def creation_teams(instace, size_player, size_team, qntTeams):
    players = []
    teams = []
    
    for i in range(size_team*qntTeams):
        players.append(creation_players(instace, size_player))

    for i in range(qntTeams):
        team = [0]
        for j in range(size_team):
            randomPlayer = random.randint(0, len(players) - 1)
            team.append(players.pop(randomPlayer))
        
        
        team_score(team)
        team = captain(team)
        teams.append(team)
    return teams

def captain(team):
    score = team[0]
    del team[0]
    team = sorted(team, key= lambda t: t[0])
    team.insert(0, score)
    return team

def team_score(team):
    ts = 0
    for i in range(len(team)):
        if( isinstance(team[i], list) ):
           ts += team[i][0]
    team[0] = ts

def dist2pt(x1, y1, x2, y2):
    Chebyschev = max(fabs(x2 - x1), fabs(y2 - y1))
    return  Chebyschev # Distancia de Chebyschev

def new_season(teams):
    for t in teams:
        t[0] = 0
    return teams

def classification(teams):
    #ordenar times, no meio da temporada e no fim da temporada
    #teams.sort(reverse = True)
    teams = sorted(teams, key= lambda t: t[0])
    return teams

'''-------------------------------------------------------------------------------'''

def training_2_opt(instace, teams, sizePayer):
    for team in teams:
        for player in team:
            if(isinstance(player, list)):
                #print(player[2]) 
                l = two_opt(player[2], instace, sizePayer)
                player[2] = l[0]
                player[0] = l[1]
                #print(player[2])
                
                    
def two_opt(player, instace, sizePayer):
    best = player
    best_score = 0
    new_score = 0
    improved = True
    while improved:
        improved = False
        for i in range(1, sizePayer-2):
            for j in range(i+1, sizePayer):
                new_player = player[:]
                new_player[i:j] = player[j-1:i-1:-1]
                best_score = score_relax(instace, best)
                new_score = score_relax(instace, new_player)
                if new_score > best_score:
                    best = new_player
                    best_score = new_score
                    improved = True
        player = best
    return [best, new_score]

#def moverSemCortar(instace, player):
def score_relax(instace, player):
    if(isinstance(player[2], list)):
        pontos_em_commum = 0
        for i in range(len(player[2]) - 1) :
            if(contem_ponto_em_comum(instace[player[2][i] - 1], instace[player[2][i + 1] - 1])):
                pontos_em_commum += 1
        return pontos_em_commum
    else:
        pontos_em_commum = 0
        for i in range(len(player) - 1) :
            if(contem_ponto_em_comum(instace[player[i] - 1], instace[player[i + 1] - 1])):
                pontos_em_commum += 1
        return pontos_em_commum

def custom_training(capitan, plaer):  
    print("cross over entre dois jogadores")

def match_day(teamM, teamV):    
    print("dia de jogo")

def transfer_phase():
    print("fase de transferencia")

def moveu_sem_cortar(instace, aresta1, aresta2):
    coordinates1 = instace[aresta1 - 1].split(" ")
    coordinates2 = instace[aresta2 - 1].split(" ")
    p1 = (coordinates1[0], coordinates1[1])
    p2 = (coordinates1[2], coordinates1[3])
    p3 = (coordinates2[0], coordinates2[1])
    p4 = (coordinates2[2], coordinates2[3])

    if(p1 == p3 or p1 == p4 or p2 == p3 or p2 == p4):
        return False
    return True

def score(instace, player, vm = 2, vc = 3):
    
    sequnciaCorte = player[2]
    senditoCorte = player[1]
    scr = 0.0
    pfX = -1.1
    pfY = -1.1
    for i in range(len(sequnciaCorte)):
        aresta = instace[sequnciaCorte[i]-1].split(" ")
        if(scr == 0):
            #estou desconsiderando o movimento do ponto de origem até o ponto inicial de corte
            dist = dist2pt(float(aresta[0]), float(aresta[1]), float(aresta[2]), float(aresta[3]))
            scr = dist * vc

            if(senditoCorte[i] == 0):
                pfX = float(aresta[2])
                pfY = float(aresta[3])
            else:
                pfX = float(aresta[0])
                pfY = float(aresta[1])   
        else:
            if(senditoCorte[i] == 0):
                pX = float(aresta[0])
                pY = float(aresta[1])
                dist = dist2pt(pfX, pfY, pX, pY)
                scr = scr + (dist * vm)
                dist = dist2pt(float(aresta[0]), float(aresta[1]), float(aresta[2]), float(aresta[3]))
                scr = scr + (dist * vc)
            else:
                pX = float(aresta[2])
                pY = float(aresta[3])
                dist = dist2pt(pfX, pfY, pX, pY)
                scr = scr + (dist * vm)
                dist = dist2pt(float(aresta[0]), float(aresta[1]), float(aresta[2]), float(aresta[3]))
                scr = scr + (dist * vc)

            if(senditoCorte[i] == 0):
                pfX = float(aresta[2])
                pfY = float(aresta[3])
            else:
                pfX = float(aresta[0])
                pfY = float(aresta[1])
               
            #pfX = eixo x no qual a maquina de corte parou ao finalizar o corte de uma aresta
            #pfY = eixo y no qual a maquina de corte parou ao finalizar o corte de uma aresta
            #pX  = eixo x no qual a maquina de corte irá inicializar o corte de uma aresta
            #pY  = eixo y no qual a maquina de corte irá inicializar o corte de uma aresta
            #(pfX, pfY) é um ponto no qual a maquina de corte parou ao finalizar o corte de uma aresta

        #descolo somando scr com vm
        #depois eu calculo somando o corte 

    return scr
    
def contem_ponto_em_comum(arestaA, arestaB):
    pontosA = arestaA.split(" ")
    pontosB = arestaB.split(" ")

    pontoA = pontosA[0] + pontosA[1]
    pontoB = pontosA[2] + pontosA[3]
    pontoC = pontosB[0] + pontosB[1]
    pontoD = pontosB[2] + pontosB[3]

    if(pontoA == pontoC or pontoA == pontoD):
        return True
    elif(pontoB == pontoC or pontoB == pontoD):
        return True
    return False


if __name__ == '__main__':
    start = time.time()
    instace = []
    sizePlay = 0
    with open("instancias/separated/instance_01_2pol.txt","r") as file:
        
        for line in file:
            if(sizePlay==0):
                sizePlay=int(line)
            elif(line != '\n'):
                if(line[-1:] == '\n'):
                    instace.append(line[:-1])
        
    teams = creation_teams(instace, sizePlay, 11, 20)
    teams = classification(teams)
    

    for k in range(5):           
        training_2_opt(instace, teams, sizePlay)
    print("########################################################################")
    '''for i in teams:
            for j in i:
                
                if( isinstance(j, list) ):
                    print(j)    
            print("--------------------------------------------------------")
            break'''
    end = time.time()
    

    '''tn = int(sys.argv[1])
    pt = int(sys.argv[2])
    genes = int(sys.argv[3])
    tq = [0] * tn
    players = initialization(genes, pt, tn)
    teams = population_division(pt, tn, players)
    '''
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
# Vm = Velocidade de movimentação da cabeça = 2
# Vc = Velocidade de corte = 4


#cada jogador tem um gene a mais, que significa sua pontuação
#cada time tem um elemento a mais que é a pontuação do time
#[5, 3, 6, 2, 8, 1, 7, 4]
#[5, 3, 6, 2, 8, 1, 7, 4]