import uuid, sys, json, os

argList = ["ajuda", "adicionar", "lista", "editar", "apagar", "pesquisar", 
		   "exportar", "importar"]
lineUp = '\033[1A'

def idInList(id,contactos):
	for contact in contactos:
		if contact['id'] == id: return True
	return False

def importHandler(ficheiro_vcf):
	"""currently importable items ['N:','TEL','EMAIL','NOTE:','UID:']"""
	while True:
		try: 
			with open(ficheiro_vcf, 'r') as file:
				c,c['name'],c['phone'],c['email'],c['note']={},(),[],[],""
				for l,line in enumerate(file):#, start=l):
					if line.find('BEGIN:VCARD') == 0: 
						print('contacto ', end='')
					elif line.find('N:') == 0: 
						c['name'] = tuple(line[2:].split(sep=';')[:2])
					elif line.find('TEL') == 0: 
						tNum = line.split(sep=';type=')[-1].split(sep=":")[-1][:-1]
						tLbl = line.split(sep=';type=')[1].split(sep=":")[0]
						numb = (tNum,tLbl)
						c['phone'].append(numb)
					elif line.find('EMAIL') == 0: 
						mail = line.split(sep=';type=')[-1].split(sep=":")[-1][:-1]
						mLbl = line.split(sep=';type=')[2].split(sep=":")[0]
						email = (mail,mLbl)
						c['email'].append(email)
					elif line.find('NOTE:') == 0:
						c['note'] = line[5:-1]
					elif line.find('UID:') == 0: 
						c['id'] = line[4:8]
						print('id ['+c['id']+']:',c['name'][1],c['name'][0], end='')
					elif line.find('END:VCARD') == 0: 
						known = idInList(c['id'],contactos)
						if not known: 
							contactos.append(c)
							print('irá ser adicionado')
						else: print('\trecusado, já na lista')
						c,c['name'],c['phone'],c['email']={},(),[],[]
						c['note']=""
				break
		except :
			print("ERRO: Arquivo de contactos não pôde ser importado."); exit()

def openContactos():
	try: 
		with open('./sources/contactos.json', 'r') as file:
			contactos = json.loads(file.read())
	except :
		if 'adicionar' == cmd: 
			print("Nenhum arquivo de contactos encontrado, criando um novo."); 
			contactos = []
		if 'importar' == cmd: 
			print("Nenhum arquivo de contactos encontrado, criando um novo."); 
			contactos = []
		else: print("ERRO: Nenhum arquivo de contactos encontrado."); exit()
	return contactos

def contactHandler(id=''):
	#variable initiations
	c = {}; c['name'] = (); c['phone'] = []; c['email'] = []; c['note'] = ""
	while True:	
		fName = input("\nInsira o PRIMEIRO nome do contacto : ")
		lName = input("Insira o ÚLTIMO nome do contacto   : ")
		if fName == '' and lName == '': continue
		else: break

	c['name'] = (lName, fName)
	while True:
		tNum  = input("\nInsira um NÚMERO de telefone       :  \n"
					+ "\t[Enter] acaso não quiser     \033[1A")
		if tNum == '': 
			print('\033[1A\x1b[2K\033[1A\x1b[2K', end='') #clean 2 above lines
			if len(c['phone']) != 0: break
			else: continue
		tLbl  = input("\tAtrelar RÓTULO ao número ? : \n"
					+ "\t[Enter] acaso não quiser     \033[1A")
		if tLbl == '': print('\x1b[2K', end='')
		numb = (tNum, tLbl)
		c['phone'].append(numb)
	print()
	while True:
		mail  = input("Atrelar um EMAIL ao contacto ?     : \n"
					+ "\t[Enter] acaso não quiser     \033[1A")
		if mail == '': 
			print('\033[1A\x1b[2K\033[1A\x1b[2K', end='') #clean 2 above lines
			mLbl = ''
			break
		else:  
			mLbl = input("\tAtrelar RÓTULO ao email ?  : \n"
					+ "\t[Enter] acaso não quiser     \033[1A")
		email = (mail, mLbl)
		c['email'].append(email)            
    
	c['note'] = input("\nAdicionar ANOTAÇÃO ao contacto ?   : \n"
					+ "\t[Enter] acaso não quiser   : \033[1A")
    
	id = str(uuid.uuid4())[0:4] if id == '' else id
	c['id'] = id

	return c	

def listContacts(contactos):
	sContactos = sorted(contactos, key=lambda d : d['name'][0])
	print( 
	f'\n'
	f'[id] | [____NOME_______]  [RÓTULO]: [_______ITEM____________________]\n'
	f'-----|----------------------------:--------------------------------- '
	)
	for c in sContactos:
		name = c['name'][1] + " " + c['name'][0]
		if len(name) < 24: print(
	f"{c['id']:<4} | {name:<24s}", end='')
		else: print(
	f"{c['id']:<4} | {c['name'][1]:<}...\n"
					f"     |      {c['name'][0]:>18} ", end='')
		for i,tel in enumerate(c['phone']): 
			if i==0 and tel[1] == '': print(
	f"Tel: {tel[0]:>12}", end='')
			elif tel[1] != '': 
				print(
	f"\n     |{tel[1]:>24} Tel: {tel[0]:>12}", end='')
			else: print(
	f"     |                          Tel: {tel[0]:>12}", end='')
		for i,mail in enumerate(c['email']): 
			if mail[0] != '': 
				print(
	f"\n     |{mail[1]:>22} eMail: {mail[0]:<12}", end='')
		if 0 < len(c['note']) <32: print(
	f"\n     |                        Nota: {c['note']:<22}", end='')
		elif len(c['note']) > 32:  
			lNote = len(c['note'])
			parts = int(lNote/32)+1 if not lNote%32 else lNote/32

			for part in range(parts):
				if part == 0: print(
	f"\n     |                        Nota: {c['note'][0:32]:<22}", end='')
				else: 
					s= part*32
					f= None if part == parts-1 else (part+1)*32
					print(f"\n     |                        "
	f"      {c['note'][s:f]:<22}", end='')
		print(
	'\n-----|----------------------------:---------------------------------|')

def yamlHandler(contactos):
	head = 'contactos'
	body = ''
	for c in contactos:
		conta = f"\n\n\t- id: {c['id']}\n\t  nome: {c['name'][1]} {c['name'][0]}\n\t  números:\n"
		tels =  "\t\t"+"\n\t\t".join(['-{}{} {}'.format(tel[1],':' if tel[1] != '' else '' ,tel[0]) for tel in c['phone']])
		mails = "" if len(c['email']) == 0 else "\n\t  emails:\n\t\t"+"\n\t\t".join(['-{}{} {}'.format(mail[1],':' if mail[1] != '' else '' ,mail[0]) for mail in c['email']])
		nota = "" if len(c['note']) == 0 else "\n\t  nota: "+ c['note']
		contact = conta+tels+mails+nota
		body += contact

	return head+body

def vCardHandler(contactos):
	''''Proof of concept, early beta stage'''
	#implement loops to catch all phones & emails
	# for c in contactos:
	c = contactos[0]
	head = 'BEGIN:VCARD\r\nVERSION:4.0\r\nPRODID:dHumanity\r\nN:'
	name = f'{c["name"][0]};{c["name"][1]}\r\nFN:{c["name"][1]} {c["name"][0]}\r\n'
	email = f'EMAIL;type=INTERNET;type={c["email"][0][1]};type=pref:{c["email"][0][0]}\r\n'
	tels = f'TEL;type={c["phone"][0][1]};type=VOICE;type=pref:{c["phone"][0][0]}\r\n'
	uid = f'UID:{c["id"]}\r\n'
	end = f'END:VCARD\r\n'
	vCard = head+name+email+tels+uid+end
	#print(c, '\n')

	return vCard

n_args = len(sys.argv[1:])
if n_args == 1:
	if sys.argv[1] in argList[:3]:
		cmd = sys.argv[1]

		if 'ajuda' == cmd: print('Utilização:\n', 
			'  python3 contactos.py [comando] [argumentos...]\n', '\n',
			'  Comandos:\n',
			'    ajuda                 Exibe esta tela de ajuda\n',
			'    adicionar             Adiciona um novo contacto\n',
			'    lista                 Apresenta a lista alfabética dos',
						  'contactos\n',
			'    editar    [id]        Edita o contacto com o', 
						  'identificador [id]\n',
			'    apagar    [id]        Elimina o contacto com o',
						  'identificador [id]\n',
			'    pesquisar [padrao]    Lista resultados da busca',
						  'por [padrao]\n',
			'    exportar  [formato]   Salva em formato [JSON],',
						  '[YAML]\n',
			'    importar  [ficheiro]  Importa de ficheiro formatado',
						  'em vCardV4')
			
		
		else: contactos = openContactos()

		if 'adicionar' == cmd:

			newContact = contactHandler()
			contactos.append(newContact)

			try:
				with open('./sources', 'r') as folder:
					folder.read()
			except FileNotFoundError: os.mkdir('sources')
			except IsADirectoryError: pass
			except: print('ERRO: diretório')
			
			with open('./sources/contactos.json', 'w') as file:
				file.write(json.dumps(contactos))
			
		if 'lista' == cmd: listContacts(contactos)

	else: print("ERRO[#argList] Comando inválido! Para ajuda use:\n",
				"python3 contactos.py ajuda. "); exit()

elif n_args == 2:
	if sys.argv[1] not in argList[3:]: 
		print("ERRO[#argList] Comando inválido! Para ajuda use:\n",
			  "python3 contactos.py ajuda. "); exit()
	
	cmd = sys.argv[1]
	arg = sys.argv[2]

	contactos = openContactos()

	if 'pesquisar' == cmd:
		ids = []
		for c in contactos: 
			if c['name'][0].find(arg) > -1 or c['name'][1].find(arg) >  -1:
				ids.append(c)
		if len(ids) > 0: listContacts(ids)
		else: print("ERRO: Termo de busca não encontrado!")
		exit()

	if 'exportar' == cmd:
		if arg.lower() == 'json':
			print(json.dumps(contactos, indent=2))
			with open('./exportado.json', 'w') as json_e:
				json_e.write(json.dumps(contactos))
		elif arg.lower() == 'yaml':
			print(yamlHandler(contactos))
			with open('./exportado.yaml', 'w') as yaml_e:
				yaml_e.write(yamlHandler(contactos))
		elif arg.lower() == 'vcard':
			print()
			print(vCardHandler(contactos), end='')
			with open('./exportado.vcf', 'w') as vCard:
				vCard.write(vCardHandler(contactos))
		exit()
	
	if 'importar' == cmd:
		vCardPath = arg
		importHandler(vCardPath)
		with open('./sources/contactos.json', 'w') as file:
				file.write(json.dumps(contactos))
		exit()

	if len(arg) != 4:  print("ERRO: Id tem 4 caracteres"); exit()
	
	contact = ''
	for i, c in enumerate(contactos):
		if c['id'].find(arg) > -1: contact = i; break

	if contact == '': print("ERRO: ID não encontrado!"); exit()
	else: id = arg 
		
	if 'editar' == cmd:
		print("Deseja EDITAR o contacto de: ", contactos[contact]['name'],"?")
		choice = input("Sim ou não ? ").upper()
		if choice == "SIM": contactos[contact] = contactHandler(id)
		else: quit()
        #break
	if 'apagar' == cmd:
		print("Deseja APAGAR o contacto de: ", contactos[contact]['name'],"?")
		choice = input("Sim ou não ? \n").upper()
		if choice == "SIM": del contactos[contact]
        #break
    
	with open('./sources/contactos.json', 'w') as file:
		file.write(json.dumps(contactos))
	exit()

# n_args == 0 | n_args >2
else: print("ERRO[#n_args] Comando inválido! Para ajuda use:\n",
			"python3 contactos.py ajuda. "); exit()
