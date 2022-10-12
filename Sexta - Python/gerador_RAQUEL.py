while True:
    titulo = input("Insira um títtulo:")
    if titulo == "":
        print("ERRO: título não pode ser vazio!")
        break
    autor = input("Insira um autor:")
    if autor == "":
        print("ERRO: autor não pode ser vazio!")
        break
    else:
        data = input("Insira a data de publicação:")

        formato = input("Insira o formato (YAML, JSON ou XML):").upper()
        ficheiro = input("Insira um nome de ficheiro:")

        if ficheiro == "":
            ficheiro = titulo

        if formato == "YAML":
            f = open(ficheiro + ".yaml", "w")
            f.write(f'titulo: {titulo} \n')
            f.write(f'autor: {autor} \n')
            f.write(f'data: {data} \n')
            f.close()

        elif formato == "":
            f = open(ficheiro + ".yaml", "w")
            f.write(f'titulo: {titulo} \n')
            f.write(f'autor: {autor} \n')
            f.write(f'data: {data} \n')
            f.close()

        elif formato == "JSON":
            f = open(ficheiro + ".json", "w")
            f.write("{\n")
            f.write('\t"titulo": "' + titulo + '",\n')
            f.write('\t"autor": "' + autor + '",\n')
            f.write('\t"data": "' + data + '"\n')
            f.write("}\n")
            f.close()

        elif formato == "XML":
            f = open(ficheiro + ".xml", "w")
            f.write('\t<obra data=' + data + '>\n')
            f.write('\t\t<titulo>' + titulo + '</titulo>\n')
            f.write('\t\t<autor>' + autor + '</autor>\n')
            f.write('\t</obra> \n')
            f.close()

        else:
            print("ERRO: Formato Inválido.")
            print("Não foi possível gerar o resultado.")
