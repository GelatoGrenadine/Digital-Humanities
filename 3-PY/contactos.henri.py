import re, sys

# Utilização:
#   python3 contactos.py [comando] [argumentos...]

#   Comandos:
#     adicionar             Adiciona um novo contacto
#     editar [id]           Edita o contacto com o identificador [id]
#     apagar [id]           Elimina o contacto com o identificador [id]
#     lista                 Apresenta a lista total de contactos por ordem alfabética
#     pesquisar [padrao]    Pesquisa e apresenta os resultados da procura por [padrao] na lista


argList = ["ajuda", "adicionar", "editar", "apagar", "lista", "pesquisar" ]

n_args = len(sys.argv[1:])
if n_args == 1:
	if sys.argv[1] in argList:
		cmd = sys.argv[1]
		print(cmd)
	else: print("ERRO[#argList] Comando inválido! Para ajuda use:\n python3 contactos.py ajuda. "); exit()
elif n_args == 2:
	if sys.argv[1] in argList:
		cmd = sys.argv[1]
	else: print("ERRO[#argList] Comando inválido! Para ajuda use:\n python3 contactos.py ajuda. "); exit()
	arg = sys.argv[2]
	print(cmd,arg)


# n_args == 0 | n_args >2
else: print("ERRO[#n_args] Comando inválido! Para ajuda use:\n python3 contactos.py ajuda. "); exit()
