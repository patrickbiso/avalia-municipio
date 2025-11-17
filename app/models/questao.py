class Questao:
    def __init__(self, numero_questao=None, texto=None, tipo=None, valor_min=None, valor_max=None, obrigatoria=True):
        self.numero_questao = numero_questao
        self.texto = texto
        self.tipo = tipo
        self.valor_min = valor_min
        self.valor_max = valor_max
        self.obrigatoria = obrigatoria
