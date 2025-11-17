class Resposta:
    def __init__(self, numero_resposta=None, numero_avaliacao=None, registro_servico=None, numero_questao=None,
                 cpf_usuario=None, texto_resposta=None, codigo_opcao=None, valor_numerico=None):
        self.numero_resposta = numero_resposta
        self.numero_avaliacao = numero_avaliacao
        self.registro_servico = registro_servico
        self.numero_questao = numero_questao
        self.cpf_usuario = cpf_usuario
        self.texto_resposta = texto_resposta
        self.codigo_opcao = codigo_opcao
        self.valor_numerico = valor_numerico
