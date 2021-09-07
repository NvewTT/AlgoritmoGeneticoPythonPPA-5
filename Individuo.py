import numpy as np


class Individuo:
    def __init__(self):
        self.genes = np.zeros(16)
        self.custoCaminho = 0
        self.roletaRangeMinimo = 0
        self.roletaRangeMaximo = 0
        self.fitnees = 0
        self.fitneesPorcentagem = 0

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
