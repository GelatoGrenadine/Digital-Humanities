# -*- coding: utf-8 -*-
import requests
import json
import unidecode

#http fetch .json file by feeding url
url = "https://api.ipma.pt/public-data/forecast/locations.json"
locations = requests.get(url).json()

def lowerAscii(input):
	return unidecode.unidecode(input).lower()

#filter ascii location list for user inputed location and return locationID
while True:
	location = lowerAscii(input("Insira uma localidade: "))
	try:
		loc = filter(lambda loc: lowerAscii(loc["local"]) == location, locations)
		idLocal = list(loc)[0]["globalIdLocal"]
		break
	except:
		print("ERRO: Localidade não econtrada!")

# guery api for by locationID and pretty print
query = "https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/" + str(idLocal) + ".json"
forecast = requests.get(query).json()
print(json.dumps(forecast, indent=2))
