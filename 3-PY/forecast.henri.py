# -*- coding: utf-8 -*-
import requests
import json
import unidecode

#http fetch .json file by feeding url
url = "https://api.ipma.pt/public-data/forecast/locations.json"
locations = requests.get(url).json()

def lowerAscii(input):
	return unidecode.unidecode(input).lower()

#compare ascii versions of both user input and location list
while True:
	location = lowerAscii(input("Insira uma localidade: "))
	try:
		for loc in locations:
			if lowerAscii(loc["local"]) == location:
				idLocal = loc["globalIdLocal"]
				break
		#extra break to get out of while loop too
		if idLocal: break
	except:
		print("ERRO: Localidade não econtrada!")

query = "https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/" + str(idLocal) + ".json"
forecast = requests.get(query).json()
print(json.dumps(forecast, indent=2))
