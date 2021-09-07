from functools import reduce
import matplotlib.pyplot as plt
from itertools import chain
from operator import itemgetter, attrgetter
import numpy as np
import random
from PPA5.Individuo import Individuo


class AG:
    # __slots__ = ['taxaCruzamento','elitismo','taxaMutacao', 'quantidadeGenes', 'novaPopulacao', 'tamanhoPopulacao', 'matrizDistancia']

    def __init__(self, tamanhoPopulacao, geracoes, caminhoDistancias, quantidadeGenes, taxaMutacao, taxaCruzamento,
                 elitismo=True):
        self.tamanhoPopulacao = tamanhoPopulacao
        self.geracoes = geracoes
        self.matrizDistancia = np.loadtxt(caminhoDistancias)
        self.quantidadeGenes = quantidadeGenes
        self.taxaMutacao = taxaMutacao
        self.taxaCruzamento = taxaCruzamento
        self.elitismo = elitismo
        self.novaPopulacao = self.iniciaPopulacao()
        self.melhorIndividuoFitnees = []
        self.melhoresIndividuos = []
        self.piorIndividuo = []
        self.mediaPopulacao = []

    def iniciaAG(self):
        for i in range(self.geracoes):
            pais = self.fitnees(self.novaPopulacao)
            filhos = self.cruzamento(pais)
            populacaoDeFilhosComPais = list(chain(pais, filhos))
            populacaoComFitneesRelativo = self.geraFitneesRelativo(populacaoDeFilhosComPais)
            populacaoOrdenadaPeloFitnees = sorted(populacaoComFitneesRelativo, key=attrgetter('fitnees'))
            self.melhorIndividuoFitnees.append(max(populacaoOrdenadaPeloFitnees, key=attrgetter('fitnees')).fitnees)
            self.melhoresIndividuos.append(max(populacaoOrdenadaPeloFitnees, key=attrgetter('fitnees')))
            self.piorIndividuo.append(min(populacaoOrdenadaPeloFitnees, key=attrgetter('fitnees')).fitnees)
            mediaPopulacao = np.mean([individuo.fitnees for individuo in populacaoOrdenadaPeloFitnees])
            self.mediaPopulacao.append(mediaPopulacao)
            print(f'Geracao: {i + 1}')
            print(f'Media da Populacao: {mediaPopulacao}')
            self.novaPopulacao = self.selecao(populacaoOrdenadaPeloFitnees)
        melhorIndividuo = max(self.melhoresIndividuos, key=attrgetter('fitnees'))
        menorRota = melhorIndividuo.genes
        menorCustoCaminho = melhorIndividuo.custoCaminho
        print(menorRota)
        print(menorCustoCaminho)
        listaDeGeracoes = np.arange(self.geracoes)
        fig1, ax1 = plt.subplots()
        ax1.grid(True)
        plt.title('AG')
        plt.xlabel('Geração')
        plt.ylabel('Fitnees')
        ax1.plot(listaDeGeracoes, self.mediaPopulacao, "r",
                 listaDeGeracoes, self.melhorIndividuoFitnees, "b",
                 listaDeGeracoes, self.piorIndividuo, "k")
        ax1.legend(('Media Global', 'Melhor Individuo', "Pior Individuo"),
                   shadow=True)
        plt.show()

    def iniciaPopulacao(self):
        populacao = []
        for i in range(self.tamanhoPopulacao):
            genesAleatorios = np.random.permutation(self.quantidadeGenes)
            individuo = Individuo()
            individuo.setGenes(genesAleatorios)
            populacao.append(individuo)
        return populacao

    def fitnees(self, populacao):
        for individou in populacao:
            custo = 0
            for i in range(len(individou.genes)):
                if i == len(individou.genes) - 1:
                    break
                custo = custo + self.distanciaEntreCidades(int(individou.genes[i]), int(individou.genes[i + 1]))
            individou.setCustoCaminho(custo)
            fitnees = 1 / custo
            individou.setFitnees(fitnees)
        return populacao

    def distanciaEntreCidades(self, cidadeAtual, proximaCidade):
        return self.matrizDistancia[cidadeAtual, proximaCidade]

    def tentePai1(self, filho, contadorfilho, pai1, contadorPai):
        if not (pai1[contadorPai] in filho):
            filho[contadorfilho] = np.copy(pai1[contadorPai])
            return True
        else:
            return False

    def tentePai2(self, filho, contadorfilho, pai2, contadorPai):
        if not (pai2[contadorPai] in filho):
            filho[contadorfilho] = np.copy(pai2[contadorPai])
            return True
        else:
            return False

    def cruzamento(self, pais):
        filhos = []
        for i in range(len(pais) - 1):
            if i % 2 == 0:
                chanceAleatoria = random.random()
                if chanceAleatoria < self.taxaCruzamento:
                    filho1 = self.geraFilho(pais[i], pais[i + 1])
                    filho2 = self.geraFilho(pais[i + 1], pais[i])
                    filhos.append(filho1)
                    filhos.append(filho2)
        filhos = self.mutacao(filhos)
        filhos = self.fitnees(filhos)
        return filhos

    def geraFilho(self, pai1, pai2):
        filho = Individuo()
        cont = 0
        controle = True
        i = 0
        while i < len(pai1.genes) - 1:
            if controle:
                if self.tentePai1(filho.genes, i, pai1.genes, cont):
                    controle = False
                    i += 1
                else:
                    if self.tentePai2(filho.genes, i, pai2.genes, cont):
                        cont += 1
                        controle = True
                        i += 1
                    else:
                        cont += 1
                        controle = True
            else:
                if self.tentePai2(filho.genes, i, pai2.genes, cont):
                    cont += 1
                    controle = True
                    i += 1
                else:
                    cont += 1
                    if self.tentePai1(filho.genes, i, pai1.genes, cont):
                        i += 1
                        controle = False
                    else:
                        controle = False
        return filho

    def mutacao(self, filhos):
        listaGenes = [i for i in range(self.quantidadeGenes)]
        for filho in filhos:
            chanceAleatoria = random.random()
            if chanceAleatoria < self.taxaMutacao:
                gene1Index = random.choice(listaGenes)
                gene2Index = random.choice(listaGenes)
                gene1 = np.copy(filho.genes[gene1Index])
                gene2 = np.copy(filho.genes[gene2Index])
                filho.genes[gene1Index] = np.copy(gene2)
                filho.genes[gene2Index] = np.copy(gene1)
        return filhos

    def geraFitneesRelativo(self, populacao):
        fitneesTotal = 0
        for individou in populacao:
            fitneesTotal += individou.fitnees
        for individou in populacao:
            individou.setFitneesPorcentagem((individou.fitnees / fitneesTotal))
        return populacao

    def selecao(self, populacao):
        populacao = self.geraRangeRoleta(populacao)
        proximaPopulacao = self.roleta(populacao)
        return proximaPopulacao

    def geraRangeRoleta(self, populacao):
        rangeDaRoleta = 0
        for i, individuo in enumerate(populacao):
            if i == 0:
                rangeDaRoleta = np.copy(individuo.fitneesPorcentagem)
                individuo.roletaRangeMinimo = np.copy(0)
                individuo.roletaRangeMaximo = np.copy(rangeDaRoleta)
            elif i == self.tamanhoPopulacao - 1:
                individuo.roletaRangeMinimo = np.copy(rangeDaRoleta)
                individuo.roletaRangeMaximo = np.copy(1)
            else:
                individuo.roletaRangeMinimo = np.copy(rangeDaRoleta)
                rangeDaRoleta += np.copy(individuo.fitneesPorcentagem)
                individuo.roletaRangeMaximo = np.copy(rangeDaRoleta)
        return populacao

    def roleta(self, populacao):
        novaPopulacao = []
        if not self.elitismo:
            for i in range(self.tamanhoPopulacao):
                chanceAleatoria = random.random()
                for individuo in populacao:
                    if (chanceAleatoria >= individuo.roletaRangeMinimo) & \
                            (chanceAleatoria <= individuo.roletaRangeMaximo):
                        novaPopulacao.append(individuo)
        else:
            quantidadesDaElite = 5
            for i in range(len(populacao) - 1, len(populacao) - (quantidadesDaElite + 1), -1):
                novaPopulacao.append(populacao[i])
            for i in range(self.tamanhoPopulacao - quantidadesDaElite):
                chanceAleatoria = random.random()
                for individuo in populacao:
                    if (chanceAleatoria >= individuo.roletaRangeMinimo) & \
                            (chanceAleatoria <= individuo.roletaRangeMaximo):
                        novaPopulacao.append(individuo)
            return novaPopulacao
