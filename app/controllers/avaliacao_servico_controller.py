from app.dao.avaliacao_servico_dao import AvaliacaoServicoDAO
from app.models.avaliacao_servico import AvaliacaoServico


class AvaliacaoServicoController:

    @staticmethod
    def adicionar_servico(numero_avaliacao, registro_servico):
        item = AvaliacaoServico(numero_avaliacao, registro_servico)
        return AvaliacaoServicoDAO.inserir(item)

    @staticmethod
    def listar(numero_avaliacao):
        return AvaliacaoServicoDAO.listar_servicos_da_avaliacao(numero_avaliacao)
