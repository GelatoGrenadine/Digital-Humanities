# -*- coding: utf-8 -*-
import json
import html
import urllib
import requests
import html5lib
from bs4 import BeautifulSoup
from lxml import etree

locais = "https://raw.githubusercontent.com/prpm-aulas/fpln-22-23/main/aula-08/previsoes/locais.json"

baseurl = "https://www.ipma.pt/pt/otempo/prev.localidade.hora/#"

locations = ["Aveiro","Beja","Braga","Bragança","Castelo Branco",
			 "Coimbra","Évora","Faro","Guarda","Leiria","Lisboa",
			 "Portalegre","Porto","Santarém","Setúbal",
			 "Viana do Castelo","Vila Real","Viseu","Madeira",
			 "Porto Santo","Santa Maria","São Miguel","Terceira",
			 "Graciosa","São Jorge","Pico","Faial","Flores","Corvo"]
LOC = list(map(lambda x: x.upper(),locations))
#LOCascii = unidecode.unidecode(LOC)
#print(LOCascii)

while True:
	location = input("Insira uma localidade: ").upper()
	try:
		i = LOC.index(location)
		location = urllib.parse.quote(locations[i])
		break
	except ValueError:
		print("ERRO: Localidade não econtrada!")

query = baseurl + location + "&" + location

print(query)

request = requests.get(query)
soup = BeautifulSoup(request.content, 'html5lib')
dom = etree.HTML(str(soup))
forecast = dom.xpath('//*[@id="weekly"]')[0].text
tMin = dom.xpath('//*[@id="11"]/span[1]')[0].text
tMax = dom.xpath('//*[@id="11"]/span[2]')[0].text
precipitaProb = dom.xpath('//*[@id="11"]/div[3]')[0].text



# {
#     "owner": "IPMA",
#     "country": "PT",
#     "data": [
#         {
#             "precipitaProb": "40.0",
#             "tMin": "12.7",
#             "tMax": "21.5",
#             "predWindDir": "SE",
#             "idWeatherType": 7,
#             "classWindSpeed": 1,
#             "longitude": "-8.6535",
#             "forecastDate": "2022-11-10",
#             "classPrecInt": 1,
#             "latitude": "40.6413"
#         }
#     ],
#     "globalIdLocal": 1010500,
#     "dataUpdate": "2022-11-10T23:31:04"
# }

# https://www.ipma.pt/pt/otempo/prev.localidade.hora/#Lisboa&Lisboa