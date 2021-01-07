    # Candidato: Isac Mendes Lacerda

    # Questão 3:


class MatrizQuadrada:
    def __init__(self, tamanho, valores):
        if isinstance(tamanho, list):
            self.tamanho = tamanho
        else:
            raise ("As dimensões da matriz precisa precisa ser expressa como 'list'!")
            self.mat = valores

        if isinstance(valores, list):
            self.tamanho = tamanho
        else:
            raise ("Os valores precisam estar em uma lista de listas!")
            self.mat = valores

    def __add__(self,m1, m2):
        if len(m1) != len(m2) or len(m1[0] != len(m2[0])):
            raise ("Dimensões não podem ser diferentes!")
        else:
            for linha in range len(m1)

    def __mul__(self, m1, m2):
        if len(m1) != len(m2):
            raise ("Dimensões não podem ser diferentes!")
