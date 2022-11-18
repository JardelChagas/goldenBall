from numpy.random import default_rng
import random
from math import fabs
import time
import copy
from itertools import combinations
from multiprocessing import Pool
import matplotlib.pyplot as plt
from matplotlib.collections import EventCollection
import numpy as np

def creation_players(instace, size):
    
    rng = default_rng()
    playerR = rng.choice(size, size=size, replace=False).tolist()
    
    for x in range(len(playerR)):
        playerR[x] = playerR[x] + 1

    playerL = [random.randint(0, 1) for i in range(size)]
     

    player = [-1, playerL, playerR]
    #player[0] = score_relax(instace, player)
    player[0] = score(instace, player)
    player.insert(3, 0)
    
    return player

def creation_teams(instace, size_player, qntTeams, size_team):
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
    teams = classification_team(teams)
    return teams

def classification_team(teams):
    return sorted(teams, key = lambda t: t[0], reverse = True)

def captain(team):
    score = team[0]
    del team[0]
    team = sorted(team, key= lambda t: t[0],reverse=True)
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
    teams = sorted(teams, key= lambda t: t[0])
    return teams

def training_2_opt(instace, teams, sizePayer):
    for team in teams:
        capitan = team[1]
        for player in team:
            if(isinstance(player, list)):
                l = two_opt(player[2], instace, sizePayer)
                
                if(player[0] == l[1] and player != capitan):
                    player[3] += 1
                
                player[2] = l[0]
                player[0] = l[1]
                sentido(instace, player)
                if(player[3] == 5):
                    player = custom_training(capitan, player, sizePayer)
                    #score_relax(instace, player)
                    score(instace, player)
                    player[3] = 0
                              
def two_opt(player, instace, sizePayer):
    best = player
    #best_score = score_relax(instace, best)
    best_score = score(instace, best)
    new_score = 0
    improved = True
    while improved:
        improved = False
        for i in range(1, sizePayer-2):
            for j in range(i+1, sizePayer):
                new_player = player[:]
                new_player[i:j] = player[j-1:i-1:-1]
                #new_score = score_relax(instace, new_player)
                new_score = score(instace, new_player)
                if new_score > best_score:
                    best = new_player
                    best_score = new_score
                    improved = True
        player = best
    return [best, best_score]

def score_relax(instace, player):
    pontos_em_commum = 0
    if(isinstance(player[2], list)):
        for i in range(len(player[2]) - 1) :
            if(contem_ponto_em_comum(instace[player[2][i] - 1], instace[player[2][i + 1] - 1])):
                pontos_em_commum += 1
        return pontos_em_commum
    else:
        for i in range(len(player) - 1) :
            if(isinstance(player, list) and contem_ponto_em_comum(instace[player[i] - 1], instace[player[i + 1] - 1])):
                pontos_em_commum += 1
        return pontos_em_commum

def aresta_visitada(arestaA, arestaB):
    pontosA = arestaA.split(" ")
    pontosB = arestaB.split(" ")

    x1 = pontosA[0] +" "+ pontosA[1]
    y1 = pontosA[2] +" "+ pontosA[3]
    x2 = pontosB[0] +" "+ pontosB[1]
    y2 = pontosB[2] +" "+ pontosB[3]

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

def setar(ponto1, ponto2, ponto3, ponto4, ponto5=(0.0,0.0), ponto6=(0.0,0.0)):
    
    sentido = -1
    
    if(ponto1 == ponto3 or ponto1 == ponto4):
        if(ponto1[0] < ponto2[0] or ponto1[1] < ponto2[1]):#se para onde eu for o ponto é maior
            sentido = 1
        else:
            sentido = 0
    elif(ponto2 == ponto3 or ponto2 == ponto4):
        if(ponto1[0] < ponto2[0] or ponto1[1] < ponto2[1]):#se para onde eu for o ponto é maior
            sentido = 0
        else:
            sentido = 1
    else:
        sentido = 1
        #if(last_setar(ponto1, ponto2, ponto5, ponto6) == 0):
        #    sentido = 1
        #else:
        #    sentido = 0
    
    return sentido

def last_setar(ponto1, ponto2, ponto3, ponto4):
    sentido = -1
    
    if(ponto1 == ponto3 or ponto1 == ponto4):
        if(ponto1[0] < ponto2[0] or ponto1[1] < ponto2[1]):#se para onde eu for o ponto é maior
            sentido = 0
        else:
            sentido = 1
    elif(ponto2 == ponto3 or ponto2 == ponto4):
        if(ponto1[0] < ponto2[0] or ponto1[1] < ponto2[1]):#se para onde eu for o ponto é maior
            sentido = 1
        else:
            sentido = 0
    else:
        a = 'não tem ponto em comum'
        sentido = 0
    
    return sentido

def sentido(instace, player):
    for i in range(len(player[2]) - 1):
        pontos = instace[player[2][i] - 1].split(" ")
        pontos1 = instace[player[2][i + 1] - 1].split(" ")
        if(i > 0):
            pontos0 = instace[player[2][i-1] - 1].split(" ")
            player[1][i] = setar((float(pontos[0]), float(pontos[1])), (float(pontos[2]), float(pontos[3])), 
                            (float(pontos1[0]), float(pontos1[1])), (float(pontos1[2]), float(pontos1[3])),
                            (float(pontos0[0]), float(pontos0[1])), (float(pontos0[2]), float(pontos0[3])))
        else:
            player[1][i] = setar((float(pontos[0]), float(pontos[1])), (float(pontos[2]), float(pontos[3])), 
                            (float(pontos1[0]), float(pontos1[1])), (float(pontos1[2]), float(pontos1[3])))
    
    pontos = instace[player[2][-1] - 1].split(" ")
    pontos1 = instace[player[2][-2] - 1].split(" ")
    player[1][-1] = last_setar((float(pontos[0]), float(pontos[1])), (float(pontos[2]), float(pontos[3])), 
                            (float(pontos1[0]), float(pontos1[1])), (float(pontos1[2]), float(pontos1[3])))
    
#[6, 4, 1, 7, 3, 5, 8, 2]
#[1, 1, 0, 1, 1, 1, 0, 0]
#def maior_ponto():

def match(team1, team2):
    t1 = 0
    t2 = 0
    game_result = 0
    
    for i in range(len(team1)):
        if(isinstance(team1[i], list)):
            if(team1[i][0] > team2[i][0]):
                t1 += 1
            elif(team1[i][0] < team2[i][0]):
                t2 += 1
    
    if(t1 > t2):
        team1[0] += 3
    elif(t1 < t2):
        team2[0] += 3
    else:
        team1[0] += 1
        team2[0] += 1
    
def criar_instance(name_instace, instace, sizePayer):
    with open(name_instace,"r") as file:
        for line in file:
            if(sizePayer == -1):
                sizePayer = int(line)
            elif(line != '\n'):
                if(line[-1:] == '\n'):
                    instace.append(line[:-1])
    return sizePayer
'''-------------------------------------------------------------------------------'''

def score(instace, player, vc = 100 / 6, vm = 400):
    
    sequnciaCorte = player[2]
    senditoCorte = player[1]
    scr = 0.0
    pfX = -1.1
    pfY = -1.1
    for i in range(len(sequnciaCorte)):
        aresta = instace[sequnciaCorte[i] - 1].split(" ")
        if(scr == 0):
            if(senditoCorte[i] == 0):
                if(float(aresta[0]) < float(aresta[2]) or float(aresta[1]) < float(aresta[3])):
                    dist = dist2pt(0.0, 0.0, float(aresta[0]), float(aresta[1]))
                    scr = dist / vm

                    pfX = float(aresta[2])
                    pfY = float(aresta[3])
                else:
                    dist = dist2pt(0.0, 0.0, float(aresta[2]), float(aresta[3]))
                    scr = dist / vm

                    pfX = float(aresta[0])
                    pfY = float(aresta[1])
            else:
                if(float(aresta[0]) < float(aresta[2]) or float(aresta[1]) < float(aresta[3])):
                    dist = dist2pt(0.0, 0.0, float(aresta[2]), float(aresta[3]))
                    scr = dist / vm
                    pfX = float(aresta[0])
                    pfY = float(aresta[1])
                else:
                    dist = dist2pt(0.0, 0.0, float(aresta[0]), float(aresta[1]))
                    scr = dist / vm
                    pfX = float(aresta[2])
                    pfY = float(aresta[3])
            
            dist = dist2pt(float(aresta[0]), float(aresta[1]), float(aresta[2]), float(aresta[3]))
            scr = scr + (dist / vc)
        else:
            auxPfX = 0.0
            auxPfY = 0.0
            if(senditoCorte[i] == 0):
                if(float(aresta[0]) < float(aresta[2]) or float(aresta[1]) < float(aresta[3])):
                    pX = float(aresta[0])
                    pY = float(aresta[1])
                    auxPfX = float(aresta[2])
                    auxPfY = float(aresta[3])
                else:
                    pX = float(aresta[2])
                    pY = float(aresta[3])
                    auxPfX = float(aresta[0])
                    auxPfY = float(aresta[1])
            else:
                if(float(aresta[0]) < float(aresta[2]) or float(aresta[1]) < float(aresta[3])):
                    pX = float(aresta[2])
                    pY = float(aresta[3])
                    auxPfX = float(aresta[0])
                    auxPfY = float(aresta[1])
                else:
                    pX = float(aresta[0])
                    pY = float(aresta[1])
                    auxPfX = float(aresta[2])
                    auxPfY = float(aresta[3])
            dist = dist2pt(pfX, pfY, pX, pY)
            scr = scr + (dist / vm)
            dist = dist2pt(float(aresta[0]), float(aresta[1]), float(aresta[2]), float(aresta[3]))
            scr = scr + (dist / vc)

            pfX = auxPfX
            pfY = auxPfY
               
            #pfX = eixo x no qual a maquina de corte parou ao finalizar o corte de uma aresta
            #pfY = eixo y no qual a maquina de corte parou ao finalizar o corte de uma aresta
            #pX  = eixo x no qual a maquina de corte irá inicializar o corte de uma aresta
            #pY  = eixo y no qual a maquina de corte irá inicializar o corte de uma aresta
            #(pfX, pfY) é um ponto no qual a maquina de corte parou ao finalizar o corte de uma aresta
    return scr

def midPoint(x1, y1, x2, y2):
    return (x1 + x2) / 2, (y1 + y2) / 2

def plotar(instace, player):
    colors = ['r', 'gray']
    if(isinstance(player, list)):
        fig1, f1_axes = plt.subplots(ncols=1, nrows=1, constrained_layout=True)
        cont = 1
        for i in range(len(player[2])):
            aresta = instace[player[2][i] - 1].split(" ")
            xs = []
            ys = []
            if(player[1][i] == 0):
                if(float(aresta[0]) < float(aresta[2]) or float(aresta[1]) < float(aresta[3])):
                    xs = [float(aresta[0]), float(aresta[2])]
                    ys = [float(aresta[1]), float(aresta[3])]
                else:
                    xs = [float(aresta[2]), float(aresta[0])]
                    ys = [float(aresta[3]), float(aresta[1])]
            else:
                if(float(aresta[0]) < float(aresta[2]) or float(aresta[1]) < float(aresta[3])):
                    xs = [float(aresta[2]), float(aresta[0])]
                    ys = [float(aresta[3]), float(aresta[1])]
                else:
                    xs = [float(aresta[0]), float(aresta[2])]
                    ys = [float(aresta[1]), float(aresta[3])]
            
            f1_axes.quiver(xs[0], ys[0], xs[1]-xs[0], ys[1]-ys[0],
                    scale_units='xy', angles='xy', scale=1, color=colors[0])
            f1_axes.annotate(str(cont), midPoint(xs[0],ys[0],xs[1],ys[1]))

            cont += 1
            if(i <= (len(player[2]) - 2) and 
                (not contem_ponto_em_comum(instace[player[2][i] - 1], instace[player[2][i + 1] - 1]))):
                xs[0] = xs[1] 
                ys[0] = ys[1]

                aresta = instace[player[2][i+1] - 1].split(" ")
                if(player[1][i + 1] == 0):
                    if(float(aresta[0]) < float(aresta[2]) or float(aresta[1]) < float(aresta[3])):
                        xs[1] = float(aresta[0])
                        ys[1] = float(aresta[1])
                    else:
                        xs[1] = float(aresta[2])
                        ys[1] = float(aresta[3])
                else:
                    if(float(aresta[0]) < float(aresta[2]) or float(aresta[1]) < float(aresta[3])):
                        xs[1] = float(aresta[2])
                        ys[1] = float(aresta[3])
                    else:
                        xs[1] = float(aresta[0])
                        ys[1] = float(aresta[1])
                
                f1_axes.quiver(xs[0], ys[0], xs[1]-xs[0], ys[1]-ys[0],
                    scale_units='xy', angles='xy', scale=1, color=colors[1])
                f1_axes.annotate(str(cont), midPoint(xs[0],ys[0],xs[1],ys[1]))
                cont += 1

        plt.title("Tempo requerido: "+ str(player[0])+"s")
        plt.show()
        plt.close()
#marker=">"

def custom_training(capitan, player, index):  
    i = 0
    num = []
    while i <len(player[2]):
        num.append(player[2][i])
        player[2][i] = 0
        i += 2
    i=0
    cont = 0
    while i < index:
        if(not capitan[2][i] in player[2]):
            player[2][cont] = capitan[2][i]
            cont += 2
        i += 1

    return player

def sequencia_corte(teams, instace):
    for team in teams:
        for player in team:
            if (isinstance(player, list)):
                player[0] = score(instace, player)

def transfer_phase(teams):
    for i in range(int(len(teams)/2)):
        teams[i][-1], teams[(i+1)*-1][1] = teams[(i+1)*-1][1], teams[i][-1]

def golden_ball(name_instace, seasons, qnt_times, qnd_jogadores):
    instace = []
    sizePayer = criar_instance(name_instace, instace, -1)
    teams = creation_teams(instace, sizePayer, qnt_times, qnd_jogadores)#criar jogadores e times
    teams = classification(teams)
    games = list(range(qnt_times))
    sequencia_games = list(combinations(games, 2))
    
    for season in range(seasons):#[1, 8, 2, 3, 5, 4, 6, 7]
        new_season(teams)
        for g in range(2 * qnt_times - 2):
            if(g == qnt_times-1):
                teams = classification_team(teams)
                transfer_phase(teams)
                sequencia_games = list(combinations(games, 2))
            
            training_2_opt(instace, teams, sizePayer)#aqui ja verifico se tem um jogador que não melhorou
            jogos = 0
            i=0
            while jogos < qnt_times/2 and i < len(sequencia_games):
                if(games[sequencia_games[i][0]] != -1 and games[sequencia_games[i][1]] != -1 ):
                    #print(sequencia_games[i])
                    games[sequencia_games[i][0]] = -1
                    games[sequencia_games[i][1]] = -1
                    team1 = teams[sequencia_games[i][0]]
                    team2 = teams[sequencia_games[i][1]]
                    match(team1, team2)
                    sequencia_games.pop(i)

                    jogos += 1
                else:
                    i += 1
            if(jogos < qnt_times/2 and i >= len(sequencia_games)):
                i -= 1
                while i < len(sequencia_games) and sum(games) * -1 == qnt_times:
                    if(games[sequencia_games[i][0]] != -1 or games[sequencia_games[i][1]] != -1 ):
                        #print(sequencia_games[i])
                        games[sequencia_games[i][0]] = -1
                        games[sequencia_games[i][1]] = -1
                        team1 = teams[sequencia_games[i][0]]
                        team2 = teams[sequencia_games[i][1]]
                        match(team1, team2)
                        sequencia_games.pop(i)
                    i -= 1
            
            games = list(range(qnt_times))#seto uma nova rodada
            
        teams = classification_team(teams)

        if(season < seasons):
            transfer_phase(teams)
    sequencia_corte(teams, instace)
    return [teams, instace]
  

if __name__ == '__main__':
    
    files = [
        'instance_01_2pol', 'instance_01_3pol', 'instance_01_4pol', 'instance_01_5pol', 'instance_01_6pol',
        'instance_01_7pol', 'instance_01_8pol', 'instance_01_9pol', 'instance_01_10pol', 'instance_01_16pol',
        'albano', 'blaz1', 'blaz2', 'blaz3', 'dighe1', 'dighe2', 'fu', 'rco1', 'rco2', 'rco3', 'shapes2', 'shapes4',
        'instance_artificial_01_26pol_hole', 'spfc_instance', 'trousers',
    ]
    tipo = ['packing', 'separated']
    qnt_seasons = 1 
    qnt_team = 20
    qnt_player_to_team = 11

    start = time.time()
    gb = golden_ball('instancias/' + tipo[0] + '/' + files[0] + '.txt', qnt_seasons, qnt_team, qnt_player_to_team)
    teams = gb[0]
    instace = gb[1]
    end = time.time() 
    
    for team in teams:
        for player in team:
            print(player)
            plotar(instace, player)
            #if(isinstance(player, list)):
            #    break
        print("-------------------------------------------------------")
    print(end - start)
    

#vc -> 16.67
#cm -> 400
#[1, 0, 1, 1, 0, 0, 0, 1]
#[8, 5, 3, 2, 7, 6, 4, 1]
