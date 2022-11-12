# -*- coding: utf-8 -*-
import requests
import json
import unidecode
#import html
#import urllib
#import html5lib
#from bs4 import BeautifulSoup
#from lxml import etree

#baseurl = "https://www.ipma.pt/pt/otempo/prev.localidade.hora/#"

url = "https://api.ipma.pt/public-data/forecast/locations.json"
request = requests.get(url).text
locationsJson = json.loads(request)

locations = {loc["globalIdLocal"]: loc for loc in locationsJson}

LOC = {}
for localId, localData in locations.items():
	for key, value in localData.items():
		if key == "local": LOC[localId] = unidecode.unidecode(value).upper()
	# for key, value in Idlocal:
 	# 	if key == "local":
 	# 		print(value)

def get_key_from_value(d, val):
    keys = [k for k, v in d.items() if v == val]
    if keys:
        return keys[0]
    return None



#locations = ["Aveiro","Beja","Braga","Bragança","Castelo Branco",
#			 "Coimbra","Évora","Faro","Guarda","Leiria","Lisboa",
#			 "Portalegre","Porto","Santarém","Setúbal",
#			 "Viana do Castelo","Vila Real","Viseu","Madeira",
#			 "Porto Santo","Santa Maria","São Miguel","Terceira",
#			 "Graciosa","São Jorge","Pico","Faial","Flores","Corvo"]

#LOC = list(map(lambda x: x.upper(),locations))

#LOCascii = unidecode.unidecode(LOC)
#print(LOCascii)

while True:
	userInput = input("Insira uma localidade: ")
	location = unidecode.unidecode(userInput).upper()
	try:
		idLocal = [k for k, v in LOC.items() if v == location][0]
		break
	except IndexError:
		print("ERRO: Localidade não econtrada!")
query = "https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/" + str(idLocal) + ".json"
print(query)
payload = requests.get(query).text
forecast = json.loads(payload)
print(json.dumps(forecast, indent=2))


#query = baseurl + location + "&" + location

#print(query)

# request = requests.get(query)
# soup = BeautifulSoup(request.content, 'html5lib')
# dom = etree.HTML(str(soup))
# forecast = dom.xpath('//*[@id="weekly"]')[0].text
# tMin = dom.xpath('//*[@id="11"]/span[1]')[0].text
# tMax = dom.xpath('//*[@id="11"]/span[2]')[0].text
# precipitaProb = dom.xpath('//*[@id="11"]/div[3]')[0].text

# https://api.ipma.pt/public-data/forecast/locations.json

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