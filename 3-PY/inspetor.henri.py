# -*- coding: utf-8 -*-
import csv, re, json, argparse

db = []

#Normalize :: double colon separated values into tsv
with open("./sources/tca.txt") as file:
    tsv = re.sub(r'{}'.format("::"), 
                 r'{}'.format("\t"), file.read(), flags=re.M)
    tsv = re.sub(r'{}'.format(" \t"), 
                 r'{}'.format("\t"), tsv, flags=re.M)
    with open("./sources/tca.tsv", 'w') as tsv_f:
        tsv_f.write(tsv)
with open('./sources/tca.tsv', 'r', newline='') as tsvfile:
    file = csv.reader(tsvfile, delimiter="\t")
    for line in file: db.append(line)

with open("./sources/plano_alimentar.json") as jf:
    pa = json.loads(jf.read())

parser = argparse.ArgumentParser(
                    prog = 'Inspector de Dieta',
                    description = 'Calcula calorias',
                    epilog = '...')
subparsers = parser.add_subparsers()

parser_validar = subparsers.add_parser('validar',
                                        help='(in)valida uma dieta')
parser_validar.add_argument('validar', action='store_true')

parser_info = subparsers.add_parser('info', 
                                        help='imprime informações calóricas')
parser_info.add_argument('info', action='store_true')

parser_total = subparsers.add_parser('total',
                    help='calcula caloria de (gordura|hidratos|proteína)')
parser_total.add_argument('total', choices=['gordura','hidratos','proteína'],  
                            action='store', nargs='?',
                            metavar='gordura|hidratos|proteína',
                            help='calcula caloria especifica do subgrupo')
args = parser.parse_args()
meals = ["pequeno-almoço", "almoço", "lanche", "jantar"]
neededCal = 66 + 13.8*pa['peso'] + 5*pa['altura'] - 6.8*pa['idade']

def appendCalToDict(pa,db):
    for line in db:
        for meal in meals:
            for item in pa[meal]:
                if line[0].lower() == item[1].lower(): 
                    item.append(int(line[1]))

def crossTabulation(i_pa,i_db,i_out,pa,db):
    out = []
    for line in db:
        for meal in meals:
            for item in pa[meal]:
                if line[i_db].lower() == item[i_pa]:
                    out.append(float(line[i_out]))
    return out



appendCalToDict(pa,db)

cal = 0
for meal in meals:
    for item in pa[meal]: cal += item[0]*item[2]*item[3]/100

if 'validar' in args:
    print('necessidade calórica diária : ', round(neededCal), 
        '\ncaloria do plano alimentar  : ', round(cal))


if 'info' in args:
    print("Imprimir informações energéticas sobre o plano\n")
    for meal in meals:
        print(meal)
        for item in pa[meal]:print(
            f"\t\t {item[1]:<34}: {item[3]:>3} kcal"
            )

if 'total' in args:
    if args.total == 'gordura' : 
        gFat = 0
        fat = crossTabulation(1,0,2,pa,db)
        for meal in meals:
            for i,item in enumerate(pa[meal]): 
                gFat += item[0]*item[2]*fat[i]/100
        print("Gordura : ", round(gFat))

    elif args.total == 'hidratos': 
        gCarb = 0
        carb = crossTabulation(1,0,3,pa,db)
        for meal in meals:
            for i,item in enumerate(pa[meal]): 
                gCarb += item[0]*item[2]*carb[i]/100
        print("Carb : ", round(gCarb))
    elif args.total == 'proteína':  
        gProt = 0
        prot = crossTabulation(1,0,4,pa,db)
        for meal in meals:
            for i,item in enumerate(pa[meal]): 
                gProt += item[0]*item[2]*prot[i]/100
        print("Prot : ", round(gProt))

    else: print('caloria do plano alimentar  : ', round(cal))
