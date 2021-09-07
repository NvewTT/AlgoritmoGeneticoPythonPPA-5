import numpy as np

from PPA5.AlgortimoGenetico import AG


tamanhoPopulacao = 200
geracoes = 100
quantidadeGenes = 16
taxaMutacao = 0.03
taxaCruzamento = 0.8
caminhoDistancias = 'distancias-1.txt'
Ag = AG(tamanhoPopulacao, geracoes, caminhoDistancias, quantidadeGenes, taxaMutacao, taxaCruzamento)
Ag.iniciaAG()

