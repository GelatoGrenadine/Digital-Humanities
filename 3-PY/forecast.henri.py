# -*- coding: utf-8 -*-
import sys, argparse
import requests, json, unidecode

#http fetch .json file by feeding url
url = "https://api.ipma.pt/public-data/forecast/locations.json"
locations = requests.get(url).json()

def lowerAscii(input):
	return unidecode.unidecode(input).lower()

n_args = len(sys.argv[1:])
minim = False
maxim = False

# Parsing sys.argv module
if    n_args == 0: print("ERRO: Não foi introduzido um local.") & exit()
arg1 = sys.argv[1]
if  n_args  > 2: print("ERRO: Introduzidos parâmetros demais.") & exit()
elif  n_args == 1:
	if "ajuda" == lowerAscii(arg1): print(str(
	"Utilização:\n" +
	"  python3 meteo.py [comando] [argumentos...]\n\n" +

	"  Comando:\n" +
	"    min - Imprimir as localidades com a temperatura mínima mais alta e mais baix\n" +
	"    max - Imprimir as localidades com a temperatura máxima mais alta e mais baix\n" +
	"    [local] [dia] - Local do qual queremos ir buscar as previsões (obrigatório)\n" +
	"                    podendo passar um dia em específico\n" +
	"                       	Ex.: Braga 1")) 				& exit()
	elif "min" == arg1: minim = True;
	elif "max" == arg1: maxim = True;
	else: location = lowerAscii(arg1)
else:
	location = lowerAscii(arg1)
	arg2 = sys.argv[2]
	try:
		dia = int(arg2)
		if dia > 5: print("ERRO: comando invalido: máximo 5 dias!"); exit()
		if dia < 1: print("ERRO: comando invalido: mínomo 1 dia!");  exit()
	except Exception as ex:
		print("ERRO: comando invalido, esperando número de dias!"); exit()

# Querying & printing model
if not(minim | maxim):
	#filter api's locations.json against user inputed location and return locationID
	while True:
		try:
			loc = filter(lambda loc: lowerAscii(loc["local"]) == location, locations)
			idLocal = list(loc)[0]["globalIdLocal"]
			break
		except: print("ERRO: Localidade não econtrada!"); exit()
	# guery api for by locationID and pretty printing
	query = str("https://api.ipma.pt/open-data/forecast/meteorology/cities/daily/"
			+ str(idLocal) + ".json")
	forecast = requests.get(query).json()
	if n_args == 1:
		print(json.dumps(forecast, indent=2)); exit()
	if n_args == 2:
		print(json.dumps(forecast['data'][0:dia], indent=2)); exit()

#fetch whole data set of Portugal then return min or max
else:
	#alt json_db = []
	#alt for loc in locations: json_db.append(loc['globalIdLocal'])
	locIds = list(map(lambda locId: locId['globalIdLocal'], locations))

#try too read written file, else query
# [ ] add logic for stale data
while True:
	try:
		f2 = open("./sources/forecasts.json")
		forecasts = json.loads(f2.read()); f2.close()
		break
	except Exception as ex:
		print("querying data, it will take up to a minute !\n"+
				"\tit will be cached for faster retrieval ")
		forecasts = []
		for loc in locIds:
			q = str("https://api.ipma.pt/open-data/"+
				"forecast/meteorology/cities/daily/" + str(loc) + ".json")
			r = requests.get(q)
			if r.status_code == 200:
				forecasts.append(r.json())
		fout = open("./sources/forecasts.json", "w");
		fout.write(json.dumps(forecasts)); fout.close()

# filtler for every item in list, maintain: data[tMax, tMin], globalIdLocal, dataUpdate
tmp = []; d=0;
for loc in forecasts:
	for day in loc["data"]:
		d+=1; tmp.append(
							[loc["globalIdLocal"],
							 loc["dataUpdate"],
							 d,
							 float(day["tMax"]),
							 float(day["tMin"])])

if maxim: print(max(tmp, key = lambda loc: loc[3]))
elif minim: print(min(tmp, key = lambda loc: loc[4]))


# To-DO
# [ ] return list of max, not just an instance
# [ ] prettify output by printing city name
