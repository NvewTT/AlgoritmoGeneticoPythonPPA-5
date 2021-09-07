import numpy as np
import random
from PPA5.Individuo import Individuo


class AG:
    __slots__ = ['taxaMutacao','quantidadeGenes','populacao', 'tamanhoPopulacao', 'matrizDistancia']

    def __init__(self, tamanhoPopulacao, matrizDistancias,quantidadeGenes,taxaMutacao):
        self.tamanhoPopulacao = tamanhoPopulacao
        self.matrizDistancia = matrizDistancias
        self.quantidadeGenes = quantidadeGenes
        self.taxaMutacao = taxaMutacao
        self.populacao = []

    def iniciaPopulacao(self):
        for i in range(self.tamanhoPopulacao):
            genesAleatorios = np.random.permutation(16)
            individuo = Individuo()
            individuo.setGenes(genesAleatorios)
            self.populacao.append(individuo)
        self.fitnees(self.populacao)

    def fitnees(self, populacao):
        for individou in populacao:
            fitnees = 0
            for i in range(len(individou.genes)):
                if i == len(individou.genes) - 1:
                    break
                fitnees = fitnees + self.distanciaEntreCidades(individou.genes[i], individou.genes[i + 1])
            individou.setFitnees(fitnees)

    def distanciaEntreCidades(self, cidadeAtual, proximaCidade):
        return self.matrizDistancia[cidadeAtual, proximaCidade]

    def tentePai1(self,filho, contadorfilho, pai1, contadorPai):
        if not (pai1[contadorPai] in filho):
            filho[contadorfilho] = pai1[contadorPai]
            return True
        else:
            return False

    def tentePai2(self,filho, contadorfilho, pai2, contadorPai):
        if not (pai2[contadorPai] in filho):
            filho[contadorfilho] = pai2[contadorPai]
            return True
        else:
            return False

    def geraFilho(self,filho, pai1, pai2):
        cont = 0
        controle = True
        i = 0
        while i < len(pai1):
            if controle:
                if self.tentePai1(filho, i, pai1, cont):
                    controle = False
                    i += 1
                else:
                    if self.tentePai2(filho, i, pai2, cont):
                        cont += 1
                        controle = True
                        i += 1
                    else:
                        cont += 1
                        controle = True
            else:
                if self.tentePai2(filho, i, pai2, cont):
                    cont += 1
                    controle = True
                    i += 1
                else:
                    cont += 1
                    if self.tentePai1(filho, i, pai1, cont):
                        i += 1
                        controle = False
                    else:
                        controle = False
        return filho

    def mutacao(self, filhos):
        for filho in filhos:
            chanceAleatoria = random.random()
            if chanceAleatoria < self.taxaMutacao:
                gene1Index = random.choice(self.quantidadeGenes)
                gene2Index = random.choice(self.quantidadeGenes)
                gene1 = filho[gene1Index]
                gene2 = filho[gene2Index]
                filho[gene1Index] = gene2
                filho[gene2Index] = gene1
        return filhos
    def geraRangeRoleta(self,populacao):
        pass
