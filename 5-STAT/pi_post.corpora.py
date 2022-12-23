import csv, time

def numerify(txt:str):
	try: 					return int(txt)
	except ValueError: 
		try: 				return float(txt)
		except ValueError: 	return txt

def emojify(val1:str, val2:str):
	d =  {'POSITIVE':'+','NEGATIVE':'-','NEUTRAL':'*'}
	return d.get(val1,' ')+'_'+d.get(val2,' ')

with open('./output/analysis.tsv', 'r', encoding='utf8') as csv_file:
    reader = csv.reader(csv_file, delimiter='\t')
    headers = next(reader)
    data = [{h:numerify(x) for (h,x) in zip(headers,row)} for row in reader]
	
"""Benchmarks automated w/ manual sentiment analisys, atributes: 
		None — if there was no manual input to compare,
		True — if they are the same,
		-1	 — if automated atributed
"""
for i,row in enumerate(data):
	# if not row['fixed_sent']: row['consoante']=	None; continue
	# if row['fixed_sent']==row['auto_sent']:
	# 	row['consoante'] = 						True
	# elif row['auto_sent']=='POSITIVE' and row['fixed_sent']=='NEUTRAL' :
	# 	row['consoante'] = 						'+_~'
	# elif row['auto_sent']=='POSITIVE' and row['fixed_sent']=='NEGATIVE':
	# 	row['consoante'] = 						'+_-'
	# elif row['auto_sent']=='NEUTRAL'  and row['fixed_sent']=='POSITIVE':
	# 	row['consoante'] = 						'~_+'
	# elif row['auto_sent']=='NEUTRAL'  and row['fixed_sent']=='NEGATIVE':
	# 	row['consoante'] = 						'~_-'
	# elif row['auto_sent']=='NEGATIVE' and row['fixed_sent']=='POSITIVE':
	# 	row['consoante'] = 						'-_+'
	# elif row['auto_sent']=='NEGATIVE' and row['fixed_sent']=='NEUTRAL':
	# 	row['consoante'] = 						'-_~'
	# else: row['consoante'] = 					print('\t\tERROR')
	row['compara'] = emojify(row['auto_sent'],row['fixed_sent'])
	print(row['compara'],'\033[1A\x1b[2K', sep='')
	time.sleep(0.016)


header 	=  list(data[0].keys())
rows	= [list(item.values()) for item in data   ]

with open('./output/analysis_newcol.tsv', 'w', encoding='utf8') as csv_file:
    csvwriter = csv.writer(csv_file, delimiter='\t')
    csvwriter.writerow(header) 
    csvwriter.writerows(rows)