import random

import numpy as np

from PPA5.AlgortimoGenetico import AG
from PPA5.Individuo import Individuo

matrizAdjacencia = np.loadtxt('distancias-1.txt')


# Ag = AG(1,matrizAdjacencia)
# Ag.iniciaPopulacao()

pai1 = np.asarray([1,2,3,4,5,6,7,8])
pai2 = np.asarray([3,7,5,1,6,8,2,4])
filho1 = np.zeros(len(pai1))


def tentePai1(filho, contadorfilho, pai1, contadorPai):
    if not (pai1[contadorPai] in filho):
        filho[contadorfilho] = pai1[contadorPai]
        return True
    else:
        return False


def tentePai2(filho, contadorfilho, pai2, contadorPai):
    if not (pai2[contadorPai] in filho):
        filho[contadorfilho] = pai2[contadorPai]
        return True
    else:
        return False


def geraFilho(filho,pai1,pai2):
    cont = 0
    controle = True
    i = 0
    while i < len(pai1):
        if controle:
            if tentePai1(filho, i, pai1, cont):
                controle = False
                i += 1
            else:
                if tentePai2(filho, i, pai2, cont):
                    cont += 1
                    controle = True
                    i += 1
                else:
                    cont += 1
                    controle = True
        else:
            if tentePai2(filho, i, pai2, cont):
                cont += 1
                controle = True
                i += 1
            else:
                cont += 1
                if tentePai1(filho, i, pai1, cont):
                    i += 1
                    controle = False
                else:
                    controle = False
    return filho


def mutacao(self,filhos,taxaMutacao):
    for filho in filhos:
        chanceAleatoria = random.random()
        if chanceAleatoria < taxaMutacao:
            quantidadeGenes = [i for i in range(len(pai1))]
            gene1Index = random.choice(quantidadeGenes)
            gene2Index = random.choice(quantidadeGenes)
            gene1 = filho[gene1Index]
            gene2 = filho[gene2Index]
            filho[gene1Index] = gene2
            filho[gene2Index] = gene1
    return filhos

print(geraFilho(filho1,pai2,pai1))
print(mutacao([filho1,np.copy(filho1)],1))