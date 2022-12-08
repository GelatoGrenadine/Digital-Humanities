# -*- coding: utf-8 -*-
import sys, itertools
import requests, json, unidecode
from datetime import datetime, date, timedelta
from termcolor import colored

#http fetch .json file by feeding url:
#url = "https://api.ipma.pt/public-data/forecast/locations.json"
url = "https://api.ipma.pt/open-data/distrits-islands.json"
locations = requests.get(url).json()['data']

def lowerAscii(input):
	return unidecode.unidecode(input).lower()

def keyReplacement(input, key1, json, key2):
	t = filter(lambda x: x[key1] == input, json)
	return  list(t)[0][key2]

def filterdByFunction(lst, lstIndex, function):
	instance = function(lst, key = lambda x: x[lstIndex])
	instances = list(filter(lambda x: x[lstIndex] == instance[lstIndex], lst))
	return instances

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
	elif "min" == arg1: minim = True
	elif "max" == arg1: maxim = True
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

#try to read written file, else query
# [✔︎] add logic for stale data
spinner = itertools.cycle(['|', '/', '-', '\\'])

while True:
	try:
		f2 = open("./sources/forecasts.json")
		forecasts = json.loads(f2.read()); f2.close()
		dataUpdate = datetime.strptime(forecasts[0]['dataUpdate'],'%Y-%m-%dT%H:%M:%S').date()
		if dataUpdate != date.today(): raise Exception
		break
	except Exception as ex:
		sys.stdout.write("No cached data, querying: \n")
		forecasts = []
		lineUp = '\033[1A'
		lineClear = '\x1b[2K'
		for loc in locIds:
			sys.stdout.write(next(spinner))   # write the next character
			sys.stdout.flush()                # flush stdout buffer (actual character display)
			sys.stdout.write('\b')            # erase the last written char

			q = str("https://api.ipma.pt/open-data/"+
				"forecast/meteorology/cities/daily/" + str(loc) + ".json")
			r = requests.get(q)
			if r.status_code == 200:
				forecasts.append(r.json())
				print(lineClear, end='')
				print("\t" + keyReplacement(loc,"globalIdLocal", locations, "local") + "\t", end='\r')

		print(lineUp,end=lineClear)
		sys.stdout.write('\033[K')		# Clear to the end of line

		fout = open("./sources/forecasts.json", "w")
		fout.write(json.dumps(forecasts)); fout.close()
		break

# filtler for every item in list, maintain: data[tMax, tMin], globalIdLocal, dataUpdate
tmp = [];
for loc in forecasts:
	d=0
	for day in loc["data"]:
		d+=1; tmp.append(
							[keyReplacement(loc["globalIdLocal"], "globalIdLocal", locations, "local"),
							 (datetime.strptime(loc["dataUpdate"],'%Y-%m-%dT%H:%M:%S')+timedelta(days=d-1)),
							 # d,
							 float(day["tMax"]),
							 float(day["tMin"])])
		#print(tmp[-1][0],"\n\t", tmp[-1][1].strftime("%a"),  colored(tmp[-1][2], 'red'),colored(tmp[-1][3], 'blue'))

if   maxim:
	max_values = filterdByFunction(tmp, 2, max)
	for i in max_values:
		print("\t\t\t\t", i[1].strftime("%a"),  colored(i[2], 'red'),i[3], "@", i[0])
		#print(M[0],"\n\t", M[1].strftime("%a"), colored(M[2], 'red'), M[3])
elif minim:
	min_values = filterdByFunction(tmp, 3, min)
	for i in min_values:
		print("\t\t\t\t", i[1].strftime("%a"), i[2], colored(i[3], 'blue'), "@", i[0])


# To-DO
# [✔︎] return list of max, not just an instance
# [✔︎] prettify output by printing city name
