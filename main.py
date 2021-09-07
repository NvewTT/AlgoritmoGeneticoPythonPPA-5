import random

import numpy as np

from PPA5.AlgortimoGenetico import AG
from PPA5.Individuo import Individuo

matrizAdjacencia = np.loadtxt('distancias-1.txt')


Ag = AG(100,matrizAdjacencia,16,0.03)
Ag.iniciaPopulacao()

pai1 = np.asarray([1,2,3,4,5,6,7,8])
pai2 = np.asarray([3,7,5,1,6,8,2,4])
filho1 = np.zeros(len(pai1))
