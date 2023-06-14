valid_symbols = "!#*()-+={}[]/"
tokens_proibidos = "wxyzt"

while True:
    contem_simbolo, contem_proibido = False, False
    print(20 * "-=")

    algarismo_latino = input("Digite um algarismo: ")
    if algarismo_latino.lower() == "sair":
        break
    
    print(f"\nVocê digitou: {algarismo_latino[0:10]}", end="\n\n")

    if algarismo_latino[0].isnumeric():
        print(f'Você digitou uma palavra reservada pelo sistema ("{algarismo_latino[0]}")', end="\n\n")

    # verifica se tem algum símbolo e caso tenha retorna True no contem simbolo
    for indice, simbolo, in enumerate(valid_symbols):
        if simbolo in algarismo_latino[0:10]:
            contem_simbolo = True
            break
    # verifica se tem algum token proibido e caso tenha verifica o contem simbolo para determinar se é uma expressão
    for indice, token, in enumerate(tokens_proibidos):
        if token in algarismo_latino[0:10].lower():
            contem_proibido = True
            print(indice)
            break
    # caso não possua simbolo roda essa parte do codigo
    if contem_proibido and not contem_simbolo:
        print("Seus algarismos contém um token não permitido,\npor favor digite novamente.")
    elif contem_proibido and contem_simbolo:
        print("É uma expressão númerica!", end="\n")
