from datetime import datetime
from operator import attrgetter

from PPA5.AlgortimoGenetico import AG
import pandas as pd
import matplotlib
import seaborn as sns;sns.set_theme()
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, plot_confusion_matrix
import numpy as np


tamanhoPopulacao = 70
geracoes = 500
quantidadeGenes = 16
taxaMutacao = 0.05
taxaCruzamento = 0.8
caminhoDistancias = 'distancias-1.txt'
mediaCustosDasPopulacoes = []
melhoresIndividuosGenes = []
melhoresIndividuos = []
quantidadesDePopulacoes = 100
for i in range(quantidadesDePopulacoes):
    Ag = AG(tamanhoPopulacao, geracoes, caminhoDistancias, quantidadeGenes, taxaMutacao, taxaCruzamento)
    melhorIndividuo, mediaPopulacao = Ag.iniciaAG(debug=True)
    print(melhorIndividuo)
    melhoresIndividuosGenes.append(melhorIndividuo.genes)
    melhoresIndividuos.append(melhorIndividuo)
    mediaCustosDasPopulacoes.append(np.mean(mediaPopulacao))



mediaGeralCusto = np.mean(mediaCustosDasPopulacoes)
desfioGeralCusto = np.std(mediaCustosDasPopulacoes)
fig1 =  plt.figure()

sns.violinplot(data=mediaCustosDasPopulacoes, palette="Set3", bw=.2, cut=1, linewidth=1)
plt.savefig(f'Ag_ViolinoPlot{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png')
dados = np.asarray(np.copy(melhoresIndividuosGenes))
frequencia = []
dados2 = np.zeros((16,16))
for i in range (16):
    frequencia.append(pd.value_counts(dados.T[i,:]))

for i in range(len(frequencia)):
    for index in frequencia[i].index:
            dados2[i,int(index)] += frequencia[i][index]

data = pd.DataFrame(dados2.T)
fig2 =  plt.figure(figsize=(15,8))
sns.heatmap(data, annot=True, annot_kws={"size": 14}, linewidths=.5)
plt.title('Heat map')
plt.xlabel('Posição')
plt.ylabel('Cidades')
plt.savefig(f'Ag_HeatMap{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.png')
print(f'Melhor individuo: {max(melhoresIndividuos, key=attrgetter("fitnees"))}')