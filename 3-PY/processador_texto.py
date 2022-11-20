from operator import itemgetter
from matplotlib import pyplot as plt
import json

# Crie uma função dicionario_para_listas que
# recebe um dicionário, e retorna 2 listas,
# uma com as chaves do dicionário e outra com
# os valores.
d = {
    "a": 1,
    "b": 2,
    "c": 3
}

chaves = []
valores = []


def dicionario_para_listas(d):
    for k in d.keys():
        chaves.append(k)
    print(chaves)

    for v in d.values():
        valores.append(v)
    print(valores)


dicionario_para_listas(d)

# A função divisao é uma função que recebe
# dois inteiros a e b e retorna o quociente
# e o resto da divisão inteira destes 2 números.


def divisao(a, b):
    q = a // b
    r = a % b
    # return q, r
    print(f'O quociente é {q}.')
    print(f'O resto é {r}.')


a = int(input('Primeiro número: '))
b = int(input('Segundo número: '))

divisao(a, b)

# Crie uma função desenha_grafico_de_barras
# que recebe o dicionário de ocorrências e
# gera um gráfico de barras que associa cada
# palavra ao seu número de ocorrências.

# Crie também uma função desenha_grafico_circular


f = open('python/aula7/words.json')
d = json.load(f)
f.close()

chaves = []
valores = []

# Ordenando para saber quais as palavras mais ocorridas no texto


def ordena_dic(d):
    return dict(sorted(d.items(), key=itemgetter(1), reverse=True))


d = ordena_dic(d)

# Selecionando as top 10 palavras mais ocorridas
for k in d.keys():
    chaves.append(k)
    chaves = chaves[0:10]

for v in d.values():
    valores.append(v)
    valores = valores[0:10]

# Função para escolher o tipo de gráfico
escolha = int(input('Escolha o tipo de gráfico: \n'
                    '1' + '.' + ' ' + 'Gráfico de Barras \n'
                    '2' + '.' + ' ' + 'Gráfico Circular \n'))


def escolha_grafico(d):
    def desenha_grafico_de_barras(d):
        x = chaves
        y = valores

        plt.bar(x, y)
        plt.show()

    def desenha_grafico_circular(d):
        labels = chaves
        valor = valores

        plt.pie(valor, labels=labels, autopct='%1.1f%%')
        plt.show()

    if escolha == 1:
        print(desenha_grafico_de_barras(d))
    elif escolha == 2:
        desenha_grafico_circular(d)
    else:
        print('Você não escolheu nenhuma opção.')
    print('Até logo!')


escolha_grafico(d)
