# Candidato: Isac Mendes Lacerda

# Questão 2
def gerar_questao(nome_origem):
    dict_arquivos = {}

    arquivo_origem = open(nome_origem, 'r')
    nr_linha = 1
    for enunciado in arquivo_origem.readlines():
        nome_arquivo_corrente = 'questao' + str(nr_linha) + '.py'
        arquivo_corrente = open(nome_arquivo_corrente, 'w')
        arquivo_corrente.write(enunciado + '\n')
        dict_arquivos['Q' + str(nr_linha)] = enunciado.split(':')[1]
        nr_linha += 1
        print(enunciado)

        arquivo_corrente.close()
    arquivo_origem.close()

    return dict_arquivos

# Principal #
print(gerar_questao('arquivo_origem'))





