# -*- coding: utf-8 -*-
import json
import html
import urllib
import requests
import html5lib
from bs4 import BeautifulSoup as bs
from lxml import etree, html

f = open("./sources/AmorDePerdição.json")
t = f.read(); f.close()
d = json.loads(t)

# http fetch file by feeding url
book = {
	"meta": {},
	"front": [],
	"chapters": [],
	"back": []
}

htmlSections = []
for page in d['pages']:
	q = str( d['URL'] + "/" + page)
	r = requests.get(q)
	if r.status_code == 200:
		soup = bs(r.content, 'html5lib')
		dom = etree.HTML(str(soup))
		#alt, access directly /div[2]/div:
		# //*[@id="mw-content-text"]/div[2]/div
		content = dom.xpath(d['XPath'])[0]
		parser = content.xpath('./div[2]')[0]
		page = parser.xpath('./div')
		h2 = dom.xpath('//*/h2')[0]
		print(parser)
		print(str(html.tostring(h2)))
		htmlSections.append(content)
		print(q)

i = 0
for section in d["pages"]:
	if i < 2:
		book["front"]=section
	else: book["chapters"]=section
	i += 1
