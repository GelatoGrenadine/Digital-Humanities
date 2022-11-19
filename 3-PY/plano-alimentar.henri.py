# -*- coding: utf-8 -*-
import csv, re, json

f1 = open("./sources/tca.txt")
tsv = re.sub(r'{}'.format("::"), r'{}'.format("\t"), f1.read(), flags=re.M)

f2 = open("./sources/plano_alimentar.json")
t2 = f2.read(); f2.close()
ex = json.loads(t2)
#print(json.dumps(ex, indent=2))

#VAR LIST:
#idade
#sexo
#peso
#altura
#pal
#pequeno-almoço
#almoço
#lanche
#jantar