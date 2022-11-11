# -*- coding: utf-8 -*-
from wordcloud import WordCloud
from matplotlib import pyplot as plt
import re

def conta(input):
	f = open(input, "r")
	t = f.read(); f.close()
	l = limpa(t).split() #clean off ponctuation & generate list of words
	d = {} #dictionary initialization
	for i in l:
		if i in d:
			d[i] += 1
		else:
			d.update({i: 1})
	return remove_stop_words(d)

def limpa(input):
	t = re.sub(r'\W', ' ', input)
	o = re.sub(r' +', ' ', t)
	return o

def remove_stop_words(input):
	stop_words = {"a", "e", "uma" ,"para" ,"um" ,"o" ,"de" ,"que" ,"se"}
	return {x: input[x] for x in input if x.lower() not in stop_words}

def desenha_nuvem(input):
	WordCloud().generate_from_frequencies(input).to_image().show()

def dicionario_para_listas(input):
	return list(input.keys()), list(input.values())

def desenha_grafico_de_barras(input, limite = 10):
  #plt.bar(dicionario_para_listas(input))
  a, b = dicionario_para_listas(input)
  a = list(a)
  b = list(b)
  ordena_duas_listas(a,b)
  plt.bar(a[:limite], b[:limite])
  plt.show()

def desenha_grafico_circular(input, limite = 10):
  #plt.bar(dicionario_para_listas(input))
  a, b = dicionario_para_listas(input)
  a = list(a)
  b = list(b)
  ordena_duas_listas(a,b)
  plt.pie(b[:limite], labels=a[:limite])
  plt.show()

def ordena_duas_listas(lista_base, outra_lista):
  lista_base_ordenada = [x for x, _ in sorted(zip(lista_base, outra_lista))]
  outra_lista_ordenada = [y for _, y in sorted(zip(lista_base, outra_lista))]

  lista_base[:] = lista_base_ordenada
  outra_lista[:] = outra_lista_ordenada

n = conta("sources/texto.txt")
print(n)
desenha_nuvem(n)

desenha_grafico_de_barras(n,10)
desenha_grafico_circular(n,10)
