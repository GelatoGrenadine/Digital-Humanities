# -*- coding: utf-8 -*-
# user data input
while True:
	titulo = input("Insira um título: ")
	try :
		if titulo != "" :
			break
		else :
			print("ERRO: Título não pode ser vazio!")
	except :
		print("ERRO: Título não pode ser vazio!")
autor = input("Insira o autor:   ")

data = input("Insira a data da publicação: ") 
formato = input("Em formato YAML, JSON ou XML: ").upper()
ficheiro = input("Insira o nome do ficheiro onde quer guardar o resultado: ")

co_autor = []

while len(co_autor) <5:
	inp =input("Insira o co-autor " + str(len(co_autor)+1) + "/5 :   ")
	if inp  == "":
		break
	if inp  in co_autor:
		print("AVISO: co-autor " + inp  + " já existe!!")
		continue
	co_autor.append(inp )
	if len(co_autor) == 5:
		print("AVISO: Limite de co-autores atingido (5/5)")

# in case filename is not provided, take title
if ficheiro == '':
	ficheiro = titulo

# outputting
if formato == "JSON" :
	co_autores = "\",\n\t\t\"".join(co_autor)
	p = str("{\n\t\"título\": \"" + titulo + "\""
		+ ",\n\t\"autor\": \"" + autor + "\""
		+ ((",\n\t\"co-autor\": [\n\t\t\"" 
		    + (co_autores + "\"\n\t]")) if len(co_autor) else "")
		+ ("" if data == "" else ",")
		+ (("\n\t\"data\": \"" + data + "\"") if data != "" else "")
		+"\n}")
	print(p)
	f = open(ficheiro + ".json", "a"); f.write(p); f.close()

elif formato == 'XML' :
	co_autores = "</co-autor>\n\t\t\t<co-autor>".join(co_autor)
	p = str("<obra" +
		(" data=\"" + data +"\"" if data != "" else "") + ">"
		+ "\n\t<titulo>" + titulo + "</titulo>"
		+ "\n\t<autor>" + autor + "</autor>"
		+ (("\n\t\t<co-autores>\n\t\t\t<co-autor>" + co_autores + "</co-autor>\n\t</co-autores>") if len(co_autor) else "")
		+ "\n</obra>")
	print(p)
	f = open(ficheiro + ".xml", "a"); f.write(p); f.close()

# defaults to YAMLm thus had "if formato == 'YAML' :" suppressed
else :
	co_autores = "\n  - ".join(co_autor)
	p = str("titulo: " + titulo
		+ "\nautor: " + autor
		+ (("\nco-autores:\n  - " + co_autores) if len(co_autor) else "")
		+ (("\ndata: " + data) if data != "" else ""))
	print(p)
	f = open(ficheiro + ".yaml", "a"); f.write(p); f.close()
