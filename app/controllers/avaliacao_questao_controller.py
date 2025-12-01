from app.dao.avaliacao_questao_dao import AvaliacaoQuestaoDAO
from app.models.avaliacao_questao import AvaliacaoQuestao


class AvaliacaoQuestaoController:

    @staticmethod
    def adicionar_questao(numero_avaliacao, numero_questao, ordem=1, peso=1):
        obj = AvaliacaoQuestao(numero_avaliacao, numero_questao, ordem, peso)
        return AvaliacaoQuestaoDAO.inserir(obj)

    @staticmethod
    def listar(numero_avaliacao):
        return AvaliacaoQuestaoDAO.listar_questoes_da_avaliacao(numero_avaliacao)
