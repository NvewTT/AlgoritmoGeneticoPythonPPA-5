import random
from itertools import chain
from operator import attrgetter

import matplotlib.pyplot as plt
import numpy as np
plt.style.use('ggplot')
from PPA5.Individuo import Individuo


class AG:
    '''Uma classe que cria roda um Algoritmo genetico

            Args:
                tamanhoPopulacao (int): Quantidade de individos na populacao
                geracoes (int): Quantidade de geracoes que o algoritmo deve executar
                caminhoDistancias (str): Caminho para o arquivo com as distancias das cidades
                quantidadeGenes (int): Quantidades de genes que o individuo tera
                taxaCruzamento (float): Chance que um individuo tem de se reproduzir
                taxaMutacao (float): Chance que um individuo tem de se mutar
                elitismo (bool): Variavel utilizada para saber se a selecao tera eletismo, por padram é definico que tenha

            Returns:
                AG: Classe contendo algoritmo genetico
            '''

    def __init__(self, tamanhoPopulacao: int, geracoes: int, caminhoDistancias: str,
                 quantidadeGenes: int, taxaCruzamento: float, taxaMutacao: float, elitismo: bool = True):
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
        self.piorIndividuoFitnees = []
        self.mediaFitneesPopulacao = []
        self.melhorIndividuoCusto = []
        self.piorIndividuoCusto = []
        self.mediaCustoPopulacao = []

    def iniciaAG(self):
        '''Função responsavel por executar o algoritmo genetico, e plotar um grafico com historicodos melhores individuos, piores e a media dos individuos


                    Returns:
                        Individuo: Objeto contendo melhor individuo
                    '''

        for i in range(self.geracoes):
            pais = self.fitnees(self.novaPopulacao)
            filhos = self.cruzamento(pais)
            populacaoDeFilhosComPais = list(chain(pais, filhos))
            populacaoComFitneesRelativo = self.geraFitneesRelativo(populacaoDeFilhosComPais)
            populacaoOrdenadaPeloFitnees = sorted(populacaoComFitneesRelativo, key=attrgetter('fitnees'))
            melhorIndividuoFitnees = max(populacaoOrdenadaPeloFitnees, key=attrgetter('fitnees'))
            self.melhorIndividuoFitnees.append(melhorIndividuoFitnees.fitnees)
            self.melhorIndividuoCusto.append(melhorIndividuoFitnees.custoCaminho)
            self.melhoresIndividuos.append(melhorIndividuoFitnees)
            piorIndividuoFitnees = min(populacaoOrdenadaPeloFitnees, key=attrgetter('fitnees'))
            self.piorIndividuoFitnees.append(piorIndividuoFitnees.fitnees)
            self.piorIndividuoCusto.append(piorIndividuoFitnees.custoCaminho)
            mediaFitneesPopulacao = np.mean([individuo.fitnees for individuo in populacaoOrdenadaPeloFitnees])
            mediaCustoPopulacao = np.mean([individuo.custoCaminho for individuo in populacaoOrdenadaPeloFitnees])
            self.mediaFitneesPopulacao.append(mediaFitneesPopulacao)
            self.mediaCustoPopulacao.append(mediaCustoPopulacao)
            print(f'Geracao: {i + 1}')
            print(f'Media fitnees da Populacao: {mediaFitneesPopulacao}'
                  f' Media custos da populacao: {mediaCustoPopulacao} ')
            self.novaPopulacao = self.selecao(populacaoOrdenadaPeloFitnees)
        melhorIndividuo = max(self.melhoresIndividuos, key=attrgetter('fitnees'))
        menorRota = melhorIndividuo.genes
        menorCustoCaminho = melhorIndividuo.custoCaminho
        print(menorRota)
        print(menorCustoCaminho)
        listaDeGeracoes = np.arange(self.geracoes)
        fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8))
        ax1.grid(True)
        ax1.set_xlabel('Gerações')
        ax1.set_ylabel('Fitnees')
        ax1.grid(True)
        ax1.plot(listaDeGeracoes, self.mediaFitneesPopulacao,
                 listaDeGeracoes, self.melhorIndividuoFitnees,
                 listaDeGeracoes, self.piorIndividuoFitnees,)
        ax1.legend(('Media Global', 'Melhor Individuo', "Pior Individuo"),
                   shadow=True)
        ax2.grid(True)
        ax2.set_xlabel('Gerações')
        ax2.set_ylabel('Custo caminho')
        ax2.grid(True)
        ax2.plot(listaDeGeracoes, self.mediaCustoPopulacao,
                 listaDeGeracoes, self.melhorIndividuoCusto,
                 listaDeGeracoes, self.piorIndividuoCusto)
        ax2.legend(('Media Global', 'Melhor Individuo', "Pior Individuo"),
                   shadow=True)
        plt.show()
        return melhorIndividuo

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
            porcentagemDeElite = 0.05
            quantidadesDaElite = int(np.around(porcentagemDeElite * self.tamanhoPopulacao,decimals=1))
            for i in range(len(populacao) - 1, len(populacao) - (quantidadesDaElite + 1), -1):
                novaPopulacao.append(populacao[i])
            for i in range(self.tamanhoPopulacao - quantidadesDaElite):
                chanceAleatoria = random.random()
                for individuo in populacao:
                    if (chanceAleatoria >= individuo.roletaRangeMinimo) & \
                            (chanceAleatoria <= individuo.roletaRangeMaximo):
                        novaPopulacao.append(individuo)
            return novaPopulacao
