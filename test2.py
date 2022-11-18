import copy

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

def score_relax(instace, player):
    pontos_em_commum = 0
    for i in range(len(player) - 1) :
        if(contem_ponto_em_comum(instace[player[i] - 1], instace[player[i + 1] - 1])):
            pontos_em_commum += 1
    return pontos_em_commum

def two_opt(route, instace):
     best = route
     improved = True
     while improved:
          improved = False
          for i in range(0, len(route)-1):
               for j in range(i+1, len(route)):
                    #if j-i == 1: continue # changes nothing, skip then
                    new_route = route[:]
                    new_route[i:j] = route[j-1:i-1:-1] # this is the 2woptSwap
                    if score_relax(instace, new_route) > score_relax(instace, best):  # what should cost be?
                         best = new_route
                         improved = True
          route = best
     return best    

if __name__ == '__main__':
    instace = []
    sizePayer = 0
    player = [0, [1, 0, 0, 1, 0, 1, 0, 0], [2, 6, 8, 3, 7, 4, 5, 1]]
    
    with open("instancias/separated/instance_01_2pol.txt","r") as file:
        sizePayer = int(file.readline(1))
        for line in file:
            if(line != '\n'):
                if(line[-1:] == '\n'):
                    instace.append(line[:-1])
    pp = [4, 5, 7, 8, 3, 6, 2, 1]
    print(pp[0:1])
    print(pp)
    print(two_opt(pp, instace))
    p = pp[:]
    p[0]  = 9

    continuar = True
    print(player)
    while(continuar):
        continuar = False
        for i in range(sizePayer-1):
            if( not contem_ponto_em_comum(instace[player[2][i] - 1], instace[player[2][i + 1] - 1]) ):
                player_copy = copy.deepcopy(player)
                gene = player_copy[2].pop(i + 1)
                player_copy[2].insert(i, gene)
                s1 = score_relax(instace, player_copy)
                s2 = score_relax(instace, player)
                            
                if( s1 > s2 ):
                    player = player_copy
                                #colocar_aresta(instace, player, gene1, gene2, i)
                    continuar = True
    print(player)