import numpy as np


class Individuo:
    '''Classe responsavel por guardar informações dos individuos

            Returns:
                Individuo: Objeto individuo
            '''
    def __init__(self):
        self.genes = np.zeros(16)
        self.custoCaminho = 0
        self.roletaRangeMinimo = 0
        self.roletaRangeMaximo = 0
        self.fitnees = 0
        self.fitneesPorcentagem = 0

    def __str__(self):
        '''Função que gera uma string contento a rota e o custo da rota.

                Returns:
                    str: Vizualização da rota e do custo da mesma
                '''
        return f'Rota : {self.genes}, custo da rota: {self.custoCaminho}'

    def setGenes(self, genes):
        self.genes = np.copy(genes)

    def setRangeRoleta(self, minimo, maximo):
        self.roletaRangeMinimo = np.copy(minimo)
        self.roletaRangeMaximo = np.copy(maximo)

    def setFitnees(self, fitnees):
        self.fitnees = np.copy(fitnees)

    def setCustoCaminho(self, custo):
        self.custoCaminho = np.copy(custo)

    def setFitneesPorcentagem(self, fitneesPorcentagem):
        self.fitneesPorcentagem = np.copy(fitneesPorcentagem)
