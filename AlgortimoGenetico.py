import numpy as np

from PPA5.Individuo import Individuo


class AG:
    __slots__ = ['populacao','tamanhoPopulacao','matrizDistancia']
    def __init__(self, tamanhoPopulacao, matrizDistancias):
        self.populacao = []
        self.tamanhoPopulacao = tamanhoPopulacao
        self.matrizDistancia = matrizDistancias

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
                if i == len(individou.genes)-1:
                    break
                fitnees = fitnees + self.distanciaEntreCidades(individou.genes[i], individou.genes[i+1])
            individou.setFitnees(fitnees)

    def distanciaEntreCidades(self, cidadeAtual, proximaCidade):
        return self.matrizDistancia[cidadeAtual, proximaCidade]