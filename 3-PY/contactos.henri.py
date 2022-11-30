import uuid, sys, json

argList = ["ajuda", "adicionar", "lista", "editar", "apagar", "pesquisar" ]

def openContactos():
	while True:
		try: 
			with open('./sources/contactos.json', 'r') as file:
				contactos = json.loads(file.read())
			break
		except :
			if 'adicionar' == cmd: 
				print("Nenhum arquivo de contactos encontrado, criando um novo."); 
				contactos = []; break
			else: print("ERRO: Nenhum arquivo de contactos encontrado."); exit()
	return contactos

def contactHandler(id=''):
	#variable initiations
	c = {}; c['name'] = (); c['phone'] = []; c['email'] = []; c['note'] = ""
	fName = input("Insira o PRIMEIRO nome do contacto : ")
	lName = input("Insira o ÚLTIMO nome do contacto   : ")
	c['name'] = (lName, fName)

	tNum  = input("Insira o NÚMERO de telefone        : ")
	tLbl  = input("\tAtrelar ID ao telefone ?\n\t[Enter] acaso não quiser   : ")
	numb = (tNum, tLbl)
	c['phone'].append(numb)

	mail  = input("Atrelar um EMAIL ao contacto ?\n\t[Enter] acaso não quiser   : ")
	mLbl  = input("\tAtrelar um ID ao email ?\n\t[Enter] acaso não quiser   : ") if mail != '' else ''
	email = (mail, mLbl)
	c['email'].append(email)            
    
	c['note'] = input("Adicionar ANOTAÇÃO ao contacto?\n\t[Enter] acaso não quiser   : ")
    
	print(id)
	id = str(uuid.uuid4())[0:4] if id == '' else id
	c['id'] = id

	return c	

n_args = len(sys.argv[1:])
if n_args == 1:
	if sys.argv[1] in argList[:3]:
		cmd = sys.argv[1]

		if 'ajuda' == cmd: print('Utilização:\n', '  python3 contactos.py [comando] [argumentos...]\n', '\n',
'  Comandos:\n',
'    ajuda                 Exibe esta tela de ajuda\n',
'    adicionar             Adiciona um novo contacto\n',
'    lista                 Apresenta a lista total de contactos por ordem alfabética\n',
'    editar [id]           Edita o contacto com o identificador [id]\n',
'    apagar [id]           Elimina o contacto com o identificador [id]\n',
'    pesquisar [padrao]    Pesquisa e apresenta os resultados da procura por [padrao] na lista')
		
		else: contactos = openContactos()

		if 'adicionar' == cmd:

			newContact = contactHandler()
			contactos.append(newContact)
			
			with open('./sources/contactos.json', 'w') as file:
				file.write(json.dumps(contactos))
		
		if 'lista' == cmd:
			print('[id] NOME e primeiro TELEFONE cadastrado')
			#sorted_footballers_by_goals = sorted(footballers_goals.items(), key=lambda x:x[1])
			sortedContactos = sorted(contactos, key=lambda d : d['name'][0])
			for c in sortedContactos:
				print('Id:',c['id'],' ',c['name'][1],c['name'][0],'\t\tTel:',c['phone'][0][0])

	else: print("ERRO[#argList] Comando inválido! Para ajuda use:\n python3 contactos.py ajuda. "); exit()

elif n_args == 2:
	if sys.argv[1] not in argList[3:]: 
		print("ERRO[#argList] Comando inválido! Para ajuda use:\n python3 contactos.py ajuda. "); exit()
	
	cmd = sys.argv[1]
	arg = sys.argv[2]

	contactos = openContactos()
	sContactos = sorted(contactos, key=lambda d : d['name'][0])

	if 'pesquisar' == cmd:
		ids = []
		for c in sContactos: 
			if c['name'][0].find(arg) > -1 or c['name'][1].find(arg) >  -1:
				ids.append(c['id'])
				print('Id:',c['id'],' ',c['name'][1],c['name'][0],'\t\tTel:',c['phone'][0][0])
		if len(ids) == 0: print("ERRO: Termo de busca não encontrado!")
		exit()

	if len(arg) != 4:  print("ERRO: Id tem 4 caracteres"); exit()
	
	contact = ''
	for i, c in enumerate(contactos):
		if c['id'].find(arg) > -1: contact = i; break

	if contact == '': print("ERRO: ID não encontrado!"); exit()
	id = arg 
		
	if 'editar' == cmd:
		print("Deseja EDITAR o contacto de: ", contactos[contact]['name'], "?")
		choice = input("Sim ou não ? \n").upper()
		if choice == "SIM": contactos[contact] = contactHandler(id)
        #break
	if 'apagar' == cmd:
		print("Deseja APAGAR o contacto de: ", contactos[contact]['name'], "?")
		choice = input("Sim ou não ? \n").upper()
		if choice == "SIM": del contactos[contact]
        #break
    
	with open('./sources/contactos.json', 'w') as file:
		file.write(json.dumps(contactos))
	exit()

# n_args == 0 | n_args >2
else: print("ERRO[#n_args] Comando inválido! Para ajuda use:\n python3 contactos.py ajuda. "); exit()
