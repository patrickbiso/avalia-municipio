from app.dao.avaliacao_dao import AvaliacaoDAO
from app.dao.resposta_dao import RespostaDAO
from app.models.resposta import Resposta

class AvaliacaoController:

    @staticmethod
    def criar_avaliacao(av):
        return AvaliacaoDAO.inserir(av)

    @staticmethod
    def registrar_resposta(numero_avaliacao, registro_servico, numero_questao, cpf_usuario,
                           texto_resposta=None, codigo_opcao=None, valor_numerico=None):

        r = Resposta(
            numero_avaliacao=numero_avaliacao,
            registro_servico=registro_servico,
            numero_questao=numero_questao,
            cpf_usuario=cpf_usuario,
            texto_resposta=texto_resposta,
            codigo_opcao=codigo_opcao,
            valor_numerico=valor_numerico
        )
        return RespostaDAO.inserir(r)
