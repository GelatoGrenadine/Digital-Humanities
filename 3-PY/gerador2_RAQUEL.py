titulo = input("Insira um títtulo:")
autor = input("Insira um autor:")

lista = []
count = 0
while True:
    coautor = input(f"Insira um co-autor ({count}/5) :")
    if coautor != "" and count < 5 and coautor not in lista:
        count = count + 1
        lista.append(coautor)
    elif coautor in lista:
        print(f'AVISO: co-autor {coautor} já existe!')
        continue
    elif coautor == "":
        break
    elif count >= 5:
        print("AVISO: Limite de co-autores atingido (5/5)")
        break

data = input("Insira a data de publicação:")
coautor = " ".join(lista)
coautor = coautor.split()

formato = input("Insira o formato (YAML, JSON ou XML):").upper()
ficheiro = input("Insira um nome de ficheiro:")

if ficheiro == "":
    ficheiro = titulo

if formato == "YAML":
    f = open(ficheiro + ".yaml", "w")
    f.write(f'titulo: {titulo} \n')
    f.write(f'autor: {autor} \n')
    f.write(f'co-autores: \n\t - {coautor[0]} \n')
    f.write(f'\t - {coautor[1]} \n')
    f.write(f'\t - {coautor[2]} \n')
    f.write(f'\t - {coautor[3]} \n')
    f.write(f'\t - {coautor[4]} \n')
    f.write(f'data: {data} \n')
    f.close()

elif formato == "JSON":
    f = open(ficheiro + ".json", "w")
    f.write("{\n")
    f.write('\t"titulo": "' + titulo + '",\n')
    f.write('\t"autor": "' + autor + '",\n')
    f.write('\t"co-autores": [ \n\t\t "' + coautor[0] + '",\n')
    f.write('\t\t "' + coautor[1] + '",\n')
    f.write('\t\t "' + coautor[2] + '",\n')
    f.write('\t\t "' + coautor[3] + '",\n')
    f.write('\t\t "' + coautor[4] + '"\n')
    f.write("], \n")
    f.write('\t"data": "' + data + '"\n')
    f.write("}\n")
    f.close()

elif formato == "XML":
    f = open(ficheiro + ".xml", "w")
    f.write('<obra data="' + data + '">\n')
    f.write('\t<titulo>' + titulo + '</titulo>\n')
    f.write('\t<autor>' + autor + '</autor>\n')
    f.write('\t<co-autores>\n')
    f.write('\t\t<co-autor>' + coautor[0] + '</co-autor>\n')
    f.write('\t\t<co-autor>' + coautor[1] + '</co-autor>\n')
    f.write('\t\t<co-autor>' + coautor[2] + '</co-autor>\n')
    f.write('\t\t<co-autor>' + coautor[3] + '</co-autor>\n')
    f.write('\t\t<co-autor>' + coautor[4] + '</co-autor>\n')
    f.write('\t</co-autores>\n')
    f.write('</obra> \n')
    f.close()
else:
    print("ERRO: Formato Inválido.")
    print("Não foi possível gerar o resultado.")
