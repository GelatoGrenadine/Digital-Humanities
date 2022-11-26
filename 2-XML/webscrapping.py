# -*- coding: utf-8 -*-
import sys, itertools, re
import requests, html, json
from bs4 import BeautifulSoup as bs
from lxml import etree
import xml.etree.cElementTree as ET
from json2xml import json2xml
from json2xml.utils import readfromurl, readfromstring, readfromjson
import struct
from xml.dom import minidom

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

#Lesssons-Learned
#	[✔︎] RegEx '(.*?)' non-greedy(?) glob(.*)

#To-LEARN
#	[ ] xml.etree.cElementTree vs lxml.etree

#To-DO
#	[ ] ADD Named Entity Recognition
#	[ ] pretty print xml, currently not properly

#Done
#	[✔︎] WebScrapped wikiSource Book content
#	[✔︎] converted to well formated .json
#	[✔︎] converted to ~~well formated~~ .xml with xml.etree
#	[✔︎] WebScrapped wikiSource Book content

"""Functions for text handling"""
#commented out lines will be handled beforehand
# #! to be dealt later
dictSubst = {
#'.^a'					: '.ª',
#!'Ill.^mo'				: <abbr expan="Illustríssimo">Ill.<sup>mo</sup></abbr>',
'ª'						: '<sup>a</sup>',
'V. Ex.<sup>a</sup>'	: '<abbr expan="Vossa Excelência">V. Ex.<sup>a</sup></abbr>',
'<i>'					: '<emph rend="italic">',
'</i>|</u>'				: '</emph>',
'<u>'					: '<emph rend="underscore">',
'<br />'				: '<lb />'
}

def substDict(text):
	text = re.sub(r'.\^([a-z]{1,3})', r'.<sup>\1</sup>', text)
	text = re.sub(r'\n\n', r'\n', text)
	for key in dictSubst:
		k = repr(key)[1:-1]; value = repr(dictSubst[k])[1:-1]
		text = re.sub(key, value, text)
	return text

def decodeHandler(text):
	return html.unescape(etree.tostring(text, pretty_print=True).decode("utf-8"))

def refsHandler(text):
	t0	= textHandler(text)
	t1	= re.sub(r'\n',r'',t0)
	t2	= re.sub(r'<ol [^>]*>(.*?)<\/ol>', r'\n<note><list type="ordered">\1</list></note>\n\n\n', t1)
	t3	= re.sub(r'<li [^>]*>(.*?)<\/li>', r'<item>\1</item>', t2)
	return t3

def titleHandler(text):
	return str("<head>" + text + "</head>\n\n")

def textHandler(text):
	t0	= decodeHandler(text)
	t1	= span_pagenumToPb(t0)
	t2	= quotationToquote(t1)
	t3	= iToEmph(t2)
	t4	= stripSpan(t3)
	t5	= newLine(t4)
	t6	= substDict(t5)
	t7	= ref(t6)
	t99 = stripA(t7)
	#print(t99)
	return t99

def newLine(text):
	add = re.sub(r'(?!\<\/p>)(.+)\n', r'\1<lb />\n', text)
	trimBack = re.sub(r'(</?\w+[^>]*> *)<lb />\n', r'\1\n', add)
	return trimBack

def stripSpan(text):
	t0	= re.sub(r'<span[^>]*>(.*?)<\/span>', r'\1', text)
	t99	= re.sub(r'<span[^>]*>|<\/span>', r'', t0)
	return t99

def stripA(text):
	t0	= re.sub(r'<a [^>]*>(.*?)<\/a>', r'\1', text)
	t1	= re.sub(r'<a [^>]*>|<\/a>', r'', t0)
	return t1

def span_pagenumToPb(text):
	return re.sub(r'(?i)<span><span class="pagenum ws-pagenum" id="([0-9]{1,3}|(XC|XL|L?X{0,3})?(IX|IV|V?I{0,3})?)".*\/><\/span>', r'<pb n="\1" />\n', text)

def quotationToquote(text):
	return re.sub(r'«(.*?)»', r'<quote>\1</quote>', text)

def iToEmph(text):
	t0	= re.sub(r'<i[^>]*>(.*?)</i>', r'<emph rend="italic">\1</emph>', text)
	t1	= re.sub(r'<i>', r'<emph rend="italic">', t0)
	t99	= re.sub(r'</i>', r'</emph>', t1)
	return t99

def ref(text):
	t0 = re.sub(r'<sup class="reference" [^>]*><a [^>]*>\[(\d+)\]</a></sup>', r'<ref><sup>\1</sup></ref>', text)
	return t0

"""UNUSED Functions for text handling"""
#https://stackoverflow.com/questions/42795042/how-to-cast-a-string-to-bytes-without-encoding
# def rawbytes(s):
#     """Convert a string to raw bytes without encoding"""
#     outlist = []
#     for cp in s:
#         num = ord(cp)
#         if num < 255:
#             outlist.append(struct.pack('B', num))
#         elif num < 65535:
#             outlist.append(struct.pack('>H', num))
#         else:
#             b = (num & 0xFF0000) >> 16
#             H = num & 0xFFFF
#             outlist.append(struct.pack('>bH', b, H))
#     return b''.join(outlist)

#def fromCodePointToUtf8(s): return re.subn('&#([0-9]{3});', lambda cp: chr(int(cp.groups()[0])) ,s)[0]
# replaced by html.unescape()

#Mockup of XML tree & assignment
root = ET.Element("TEI.2"); 
if True:
	tH	= ET.SubElement(root,"teiHeader")
	txt	= ET.SubElement(root,"text")
	frt	= 	ET.SubElement(txt,"front")
	d1f	= 		[ET.SubElement(frt,"div1") for i in range(1)]
	#d2f	= 			[ET.SubElement(d1f[0],"div2") for i in range(len(d1f)*2)]
	bod	= 	ET.SubElement(txt,"body")
	d1b	= 		[ET.SubElement(bod,"div1") for i in range(2)]
	#d2b1	= 			[ET.SubElement(d1b[0],"div2") for i in range(10)]
	#d2b2	= 			[ET.SubElement(d1b[1],"div2") for i in range(10)]
	
	#mockTree = ET.ElementTree(r)
	#mockTree.write("MockTree.xml")

#Mockup of book as dictionary/json structure
book = {
	"meta": {},
	"front": [],
	"chapters": [],
	"back": []
}

# command line niceties
spinner = itertools.cycle(['|', '/', '-', '\\'])
lineUp = '\033[1A'
lineClear = '\x1b[2K'

# loading data on where to find book
with  open("./sources/AmorDePerdição.json", 'r') as f:
    d = json.load(f)

sys.stdout.write("No cached data, querying: \n")
# http fetch file by feeding url and feeding nested lists
htmlSections = []; xmlSections = []; pg = 0
for page in d['pages']:
	print(lineClear, end ='\r')
	sys.stdout.write(next(spinner))   # write the next character
	sys.stdout.flush()                # flush stdout buffer (actual character display)
	sys.stdout.write('\b')		       # erase the last written char
	print("\tparsing:", page)
	print(lineUp,end=lineClear)

	q = str( d['URL'] + "/" + page)
	r = requests.get(q)
	if r.status_code == 200:
		soup 	= bs(r.content, 'lxml')
		dom 	= etree.HTML(str(soup))
		content = dom.xpath('//*[@id="mw-content-text"]/div[1]')[0]
		refs 	= content.xpath('//*[@class="references"]')
		title 	= content.xpath('./div//span[@class="mw-headline"]/text()')
		if len(title) > 1: title = title[0] 
		text 	= content.xpath('./div/p')

		"""HTML list [h2, p, ol] -> [<head>, <p>, <note>]"""
		htmlSections.append([
					"".join([titleHandler(t) for t in title]),
					"".join([textHandler(p ) for p in text]),
					"".join([refsHandler(r ) for r in refs])])
		
		"""XML list <div2>[<head>, <p>, <note>]"""
		ch = pg-1; 
		div2child = "".join([htmlSections[-1][0],htmlSections[-1][1],htmlSections[-1][2]])
		if   pg == 0: 
			xmlSections.append(ET.XML("".join([
								"<div2 type='Dedicatória'>", 
									htmlSections[-1][0],
									htmlSections[-1][1],
									htmlSections[-1][2], 
								"</div2>"
								])))
			d1f[0].set("type", "Prefácio")
			d1f[0].append(xmlSections[-1])
		elif pg == 1:
			xmlSections.append(ET.XML("<div2 type='Prefácio'>"+div2child+"</div2>"))
			d1f[0].append(xmlSections[-1])
		elif pg < 11: 
			xmlSections.append(ET.XML("<div2 chapter='"+str(ch)+"'>"+div2child+"</div2>"))
			d1b[0].set("type", "Parte 1")
			d1b[0].append(xmlSections[-1])
		else: 
			xmlSections.append(ET.XML("<div2 chapter='"+str(ch)+"'>"+div2child+"</div2>"))
			d1b[1].set("type", "Parte 2")
			d1b[1].append(xmlSections[-1])

		"""Dict variable for JSON export"""
		if 		pg == 0: book["front"].append({"div2 chapter='Dedicatória'" :div2child})
		elif 	pg == 1: book["front"].append({"div2 chapter='Prefácio'" 	:div2child})
		else:		 book[ "chapters"].append({"div2 chapter='"+str(ch)+"'" :div2child})
		
		pg+=1

#XML output
tree = ET.ElementTree(root)
tree.write("tTree.xml", encoding="utf-8", xml_declaration=True)
with open("tTree.xml", "r") as read:
	xml = read.read()
	with open("tTree.xml", "w") as file:
		file.write(minidom.parseString(xml).toprettyxml(indent="	"))

#JSON output & convert to XML
with open('./sources/CASTELO-BRANCO,Camilo-AmorDePerdição.json', 'w') as jsonf:
	jsonf.write(json.dumps(book, ensure_ascii=False)) 
	with open('./json2xm.xml', 'w') as xmlf:
		data = readfromjson('./sources/CASTELO-BRANCO,Camilo-AmorDePerdição.json')
		xmlf.write(html.unescape(json2xml.Json2xml(data).to_xml()))