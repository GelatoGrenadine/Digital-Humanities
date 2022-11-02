# -*- coding: utf-8 -*-
#from wordcloud import WordCloud
import re

def conta(input):
	f = open(input, "r"); t = f.read(); f.close()
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


n = conta("sources/texto.txt")
print(n)
#desenha_nuvem(n)