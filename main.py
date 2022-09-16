from cgitb import reset
from numpy.random import default_rng
#import sys
from copy import copy
import numpy as np
import random
from math import fabs

def creation_players(instace, size):
    
    rng = default_rng()
    playerL = rng.choice(size, size=size, replace=False)
    for x in range(len(playerL)):
        playerL[x] = playerL[x] + 1

    playerR = [random.randint(0, 1) for i in range(size)]
     
    for i in playerL:
        playerR.append(i)

    playerR.insert(0, score(instace, playerR))
    return playerR

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
        captain(team)
        teams.append(team)
    return teams

def captain(team):
    score = team[0]
    del team[0]
    team.sort(reverse=True)
    team.insert(0, score)

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
    teams.sort(reverse = True)

def training():
    print("treinamento dos jogadores")

def custom_training():  
    print("treino custumizado")

def match_day():    
    print("dia de jogo")

def transfer_phase():
    print("fase de transferencia")

def score(instace, player, vm = 2, vc = 3):
    
    sequnciaCorte = player[len(instace):]
    senditoCorte = player[:len(instace)]
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
    #calcular o custo dessa função
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
    instace = []
    with open("instancias/separated/instance_01_2pol.txt","r") as file:
        sizePlay = int(file.readline(1))
        for line in file:
            if(line != '\n'):
                if(line[-1:] == '\n'):
                    instace.append(line[:-1])
        
    teams = creation_teams(instace, sizePlay, 11, 20)
    #new_season(teams)
    classification(teams)
    
    for i in teams:
        for j in i:
             if( isinstance(j, list) ):
                print(j[0] if j[0] > 9 else "0" + str(j[0]), j[1:sizePlay+1], j[sizePlay+1:])
        print("----------------------------------------------------")
    #print(instace)
    print(dist2pt(100.0, 100.0, 0.0, 100.0))

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
    
