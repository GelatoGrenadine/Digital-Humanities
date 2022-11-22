# -*- coding: utf-8 -*-
import json
import html
import urllib
import requests
import html5lib
from bs4 import BeautifulSoup as bs
from lxml import etree, html as lxlhtml
import sys, itertools
import re

# as html.unescape()
#def fromCodePointToUtf8(s): return re.subn('&#([0-9]{3});', lambda cp: chr(int(cp.groups()[0])) ,s)[0]

#commented out lines will be handled beforehand
dictSubst = {
			#'.^a'									: '.ª',
			'ª'										: '<sup>a</sup>',
		    'V. Ex.<sup>a</sup>'					: '<abbr expan="Vossa Excelência">V. Ex.<sup>a</sup></abbr>',
			'<i>'									: '<emph rend="italic">',
			'</i>|</u>'								: '</emph>',
			'<u>'									: '<emph rend="underscore">',

}


def substDict(texto):
	texto = re.sub(r'.\^a', '.ª', texto)
	for key in dictSubst:
		k = repr(key)[1:-1]; value = repr(dictSubst[k])[1:-1]
		texto = re.sub(key, value, texto)
	return texto


def textHandler(text):
	t0	= html.unescape(etree.tostring(text, pretty_print=True).decode("utf-8"))
	t1	= span_pagenumToPb(t0)
	t2	= quotationToquote(t1)
	t3	= iToEmph(t2)
	t4	= stripSpan(t3)
	t5	= newLine(t4)
	t6	= substDict(t5)
	t7 = ref(t6)
	t99 = stripA(t7)
	return t99

def newLine(text):
	add = re.sub(r'(?!\<\/p>)(.+)\n', r'\1<lb />\n', text)
	trimBack = re.sub(r'(</?\w+[^>]*> *)<lb />\n', r'\1\n', add)
	return trimBack

def stripSpan(text):
	t0	= re.sub(r'<span[^>]*>(.*)<\/span>', r'\1', text)
	t99	= re.sub(r'<span[^>]*>|<\/span>', r'', t0)
	return t99

def stripA(text):
	t0	= re.sub(r'<a[^>]*>(.*)<\/a>', r'\1', text)
	t1	= re.sub(r'<a[^>]*>|<\/a>', r'', t0)
	return t1

def span_pagenumToPb(text):
	return re.sub(r'(?i)<span><span class="pagenum ws-pagenum" id="([0-9]{1,3}|(XC|XL|L?X{0,3})?(IX|IV|V?I{0,3})?)".*\/><\/span>', r'<pb n="\1" />\n', text)

def quotationToquote(text):
	return re.sub(r'«(.*)»', r'<quote>\1</quote>', text)

def iToEmph(text):
	t0	= re.sub(r'<i[^>]*>(.*)</i>', r'<emph rend="italic">\1</emph>', text)
	t1	= re.sub(r'<i>', r'<emph rend="italic">', t0)
	t99	= re.sub(r'</i>', r'</emph>', t1)
	return t99

def ref(text):
	return re.sub(r'<sup class="reference" [^>]*><a [^>]*>\[(\d+)\]</a></sup>', r'<ref><sup>\1</sup><\\ref>', text)

# command line niceties
spinner = itertools.cycle(['|', '/', '-', '\\'])
lineUp = '\033[1A'
lineClear = '\x1b[2K'

f = open("./sources/AmorDePerdição.json")
t = f.read(); f.close()
d = json.loads(t)

# http fetch file by feeding url
htmlSections = []
for page in d['pages']:
	q = str( d['URL'] + "/" + page)
	r = requests.get(q)
	if r.status_code == 200:
		soup 	= bs(r.content, 'lxml')
		dom 	= etree.HTML(str(soup))
		content = dom.xpath('//*[@id="mw-content-text"]/div[1]')[0]
		refs 	= content.xpath('//*[@class="references"]')
		title 	= content.xpath('./div//span[@class="mw-headline"]/text()')
		text 	= content.xpath('./div/p')
		sys.stdout.write(next(spinner))   # write the next character
		sys.stdout.flush()                # flush stdout buffer (actual character display)
		sys.stdout.write('\b')            # erase the last written char
		print(lineClear, end='')
		#print("\t" + html.unescape(etree.tostring(title[0], pretty_print=True).decode("utf-8")) + "\t", end='\r')
		htmlSections.append(
							[title,
							[textHandler(p) for p in text],
							refs])
		#print(etree.tostring(text[1], pretty_print=True))

for section in htmlSections:
	for p in section[1]:
		p = "".join(p)


book = {
	"meta": {},
	"front": [],
	"chapters": [],
	"back": []
}
i = -1
for section in htmlSections:
	if i < 2:
		book["front"].append({i:"".join(section[1])})
	else: book["chapters"].append({i:"".join(section[1])})
	i += 1

with open('./sources/CASTELO-BRANCO,Camilo-AmorDePerdição.json', 'w') as convert_file:
     convert_file.write(json.dumps(book))
