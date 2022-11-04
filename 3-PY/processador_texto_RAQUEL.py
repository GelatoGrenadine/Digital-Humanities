from operator import itemgetter
from matplotlib import pyplot as plt

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

d = {'era': 7, 'vez': 3, 'dois': 5, 'homens': 8, 'alto': 1, 'outro': 13, 'baixo': 5, 'gordo': 1, 'magro': 1, 'moreno': 1, 'ruivo': 1, 'tinha': 2, 'voz': 1, 'muito': 5, 'grossa': 1, 'borbulha': 1, 'na': 5, 'ponta': 1, 'do': 4, 'nariz': 1, 'chamava-se': 1, 'manuel': 2, 'francisco': 2, 'mais': 8, 'coisas': 1, 'poderia': 1, 'dizer': 1, 'cada': 4, 'deles': 1, 'fundamental': 1, 'é': 2, 'eram': 4, 'diferentes': 1, 'só': 3, 'numa': 1, 'coisa': 1, 'assemelhavam': 1, 'ambos': 1, 'tremendamente': 1, 'teimosos': 2, 'terra': 3, 'onde': 2, 'viviam': 1, 'havia': 1, 'ladeira': 12, 'íngreme': 1, 'inclinada': 1, 'cheia': 1, 'pedras': 2, 'calhaus': 2, 'daquelas': 1, 'gente': 1, 'sobe': 1, 'desce': 1, 'quando': 2, 'não': 5, 'pode': 1, 'deixar': 1, 'ser': 1, 'dia': 2, 'dos': 1, 'ia': 4, 'subir': 2, 'vinha': 2, 'descê-la': 1, 'como': 2, 'natural': 1, 'encontraram-se': 2, 'meio': 7, 'bem': 1, 'exactamente': 1, 'tenho': 1, 'certeza': 1, 'foi': 3, 'talvez': 1, 'tenha': 1, 'sido': 1, 'bocadinho': 2, 'para': 13, 'cima': 4, 'nossa': 1, 'história': 1, 'esse': 1, 'pormenor': 1, 'tem': 1, 'grande': 1, 'importância': 1, 'por': 3, 'isso': 2, 'vamos': 1, 'fazer': 2, 'conta': 1, 'menos': 3, 'pararam': 1, 'à': 4, 'frente': 1, 'desataram': 1, 'discutir': 4, 'achava': 1, 'subida': 3, 'descer': 1, 'pelo': 1, 'contrário': 1, 'garantia': 1, 'tratava': 1, 'descida': 3, 'sem': 4, 'chegar': 1, 'acordo': 1, 'sentaram-se': 1, 'ali': 2, 'mesmo': 1, 'no': 2, 'chão': 1, 'tirar': 1, 'questão': 1, 'limpo': 1, 'quem': 1, 'conhecesse': 1, 'sabendo': 1, 'palavra': 1, 'fácil': 1, 'capazes': 2, 'inventar': 1, 'sólidas': 1,
     'razões': 1, 'grandes': 1, 'argumentos': 1, 'logo': 1, 'via': 1, 'aquela': 2, 'discussão': 4, 'demorar': 1, 'demorou': 1, 'passaram-se': 2, 'sete': 4, 'dias': 2, 'noites': 2, 'parava': 1, 'veio': 2, 'lua': 2, 'foi-se': 2, 'sol': 3, 'nem': 6, 'frio': 2, 'calor': 1, 'chuva': 2, 'distraíram': 1, 'continuavam': 3, 'mesma': 2, 'porque': 2, 'subia': 2, 'descia': 2, 'continuou': 2, 'sétima': 1, 'noite': 1, 'começou': 1, 'soprar': 1, 'vento': 6, 'forte': 2, 'tão': 2, 'violento': 1, 'arrancava': 1, 'terras': 1, 'árvores': 1, 'atirava': 1, 'sítio': 1, 'daqueles': 1, 'trabalhar': 3, 'lentamente': 1, 'séculos': 2, 'fio': 1, 'mudar': 1, 'face': 1, 'transformar': 1, 'montes': 1, 'covas': 1, 'fundas': 1, 'buracos': 1, 'meter': 1, 'medo': 1, 'nas': 1, 'altas': 1, 'montanhas': 1, 'tempo': 1, 'passou': 1, 'mexeu': 1, 'com': 1, 'tudo': 1, 'mudou': 1, 'paisagem': 1, 'transformou': 1, 'mundo': 1, 'sentados': 1, 'darem': 1, 'nada': 2, 'acontecia': 1, 'sua': 1, 'volta': 2, 'estavam': 1, 'preocupados': 1, 'ganhar': 1, 'sentiram': 1, 'pele': 1, 'nos': 1, 'ossos': 1, 'moleirinha': 1, 'mil': 2, 'pouco': 2, 'ficando': 1, 'diferente': 1, 'parte': 4, 'alta': 2, 'baixa': 2, 'crescer': 1, 'parar': 1, 'custa': 1, 'entulho': 1, 'areia': 1, 'pedrinhas': 1, 'tornavam': 1, 'belo': 1, 'ficaram': 1, 'iguais': 1, 'altura': 2, 'portanto': 1, 'desapareceu': 1, 'ficou': 1, 'direitinha': 1, 'lisa': 1, 'planície': 1, 'estendia': 1, 'até': 2, 'perder': 1, 'vista': 2, 'lado': 2, 'eu': 1, 'já': 1, 'disse': 1, 'certa': 1, 'olharam': 1, 'podia': 1, 'alcançar': 1, 'aperceberam-se': 1, 'então': 1, 'desaparecido': 1, 'olhara': 1}

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
