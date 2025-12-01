from app.dao.resposta_dao import RespostaDAO

class RelatorioController:

    @staticmethod
    def ranking_servicos(top_n=10):
        return RespostaDAO.media_por_servico(limit=top_n)

    @staticmethod
    def media_secretarias():
        return RespostaDAO.media_por_secretaria()

    @staticmethod
    def evolucao_mensal(numero_avaliacao=None, registro_servico=None):
        return RespostaDAO.evolucao_mensal(numero_avaliacao, registro_servico)

    @staticmethod
    def distribuicao(numero_avaliacao, numero_questao):
        return RespostaDAO.distribuicao_por_questao(numero_avaliacao, numero_questao)
