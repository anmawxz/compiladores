def transformar_para_greibach(gramatica):
    # aqui remove producoes vazias
    anulaveis = encontrar_nao_terminais_anulaveis(gramatica)
    gramatica = remover_producoes_vazias(gramatica, anulaveis)

    # remove producoes unitárias
    producoes_unitarias = encontrar_producoes_unitarias(gramatica)
    gramatica = remover_producoes_unitarias(gramatica, producoes_unitarias)

    # renomeiaa nao terminais
    gramatica_renomeada = renomear_nao_terminais(gramatica)

    # converte producoes para a forma normal de greibach
    gramatica_greibach = converter_para_forma_greibach(gramatica_renomeada)

    return gramatica_greibach


def encontrar_nao_terminais_anulaveis(gramatica):
    anulaveis = set()
    producoes = gramatica.values()

    while True:
        nao_terminais_anulaveis_atualizados = anulaveis.copy()

        for nao_terminal, regras in producoes:
            for regra in regras:
                e_anulavel = True

                for simbolo in regra:
                    if simbolo.isupper() and simbolo not in anulaveis:
                        e_anulavel = False
                        break

                if e_anulavel:
                    nao_terminais_anulaveis_atualizados.add(nao_terminal)
                    break

        if nao_terminais_anulaveis_atualizados == anulaveis:
            break

        anulaveis = nao_terminais_anulaveis_atualizados

    return anulaveis

#remove onde possui lambda
def remover_producoes_vazias(gramatica, anulaveis):
    nova_gramatica = {}

    for nao_terminal, regras in gramatica.items():
        novas_regras = []

        for regra in regras:
            if regra == 'λ':
                novas_regras.append('')
                continue

            for combinacao in gerar_combinacoes(regra, anulaveis):
                novas_regras.append(combinacao)

        nova_gramatica[nao_terminal] = novas_regras

    return nova_gramatica


def gerar_combinacoes(regra, anulaveis):
    combinacoes = ['']

    for simbolo in regra:
        if simbolo in anulaveis:
            novas_combinacoes = []

            for combinacao in combinacoes:
                novas_combinacoes.append(combinacao + simbolo)
                novas_combinacoes.append(combinacao)

            combinacoes = novas_combinacoes
        else:
            combinacoes = [combinacao + simbolo for combinacao in combinacoes]

    return combinacoes


def encontrar_producoes_unitarias(gramatica):
    producoes_unitarias = {}

    for nao_terminal, regras in gramatica.items():
        for regra in regras:
            if len(regra) == 1 and regra.isupper():
                producoes_unitarias.setdefault(nao_terminal, set()).add(regra)

    return producoes_unitarias

#remove os unitarios
def remover_producoes_unitarias(gramatica, producoes_unitarias):
    nova_gramatica = gramatica.copy()

    while True:
        producoes_unitarias_atualizadas = {}

        for nao_terminal, unidades in producoes_unitarias.items():
            novas_regras = []

            for regra in gramatica.get(nao_terminal, []):
                if regra in producoes_unitarias:
                    novas_regras.extend(gramatica[regra])
                else:
                    novas_regras.append(regra)

            nova_gramatica[nao_terminal] = novas_regras

            producoes_unitarias_atualizadas.update(encontrar_producoes_unitarias({nao_terminal: novas_regras}))

        if producoes_unitarias_atualizadas == producoes_unitarias:
            break

        producoes_unitarias = producoes_unitarias_atualizadas

    return nova_gramatica


def renomear_nao_terminais(gramatica):
    nao_terminais = list(gramatica.keys())
    gramatica_renomeada = {}

    for i, nao_terminal in enumerate(nao_terminais):
        gramatica_renomeada['N' + str(i)] = gramatica[nao_terminal]

    return gramatica_renomeada

#verifica as regras e converte
def converter_para_forma_greibach(gramatica):
    gramatica_greibach = {}

    for nao_terminal, regras in gramatica.items():
        novas_regras = []

        for regra in regras:
            prefixo = [simbolo for simbolo in regra if simbolo.isupper()]
            sufixo = [simbolo for simbolo in regra if not simbolo.isupper()]

            if not prefixo:
                prefixo.append('λ')

            novas_regras.append(prefixo + sufixo)

        gramatica_greibach[nao_terminal] = novas_regras

    return gramatica_greibach


# primeira questao letra a)
gramatica = {
    'S': ['AB', 'SCB'],
    'A': ['aA', 'C'],
    'B': ['bB', 'b'],
    'C': ['cC', 'λ']
}

#imprime resultado
gramatica_greibach = transformar_para_greibach(gramatica)
print(gramatica_greibach)
