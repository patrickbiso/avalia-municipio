from app.dao.avaliacao_servico_dao import AvaliacaoServicoDAO

class AvaliacaoServicoController:

    @staticmethod
    def adicionar_servico(numero_avaliacao, registro_servico):
        item = AvaliacaoServicoDAO.inserir(
            item=AvaliacaoServico(numero_avaliacao, registro_servico)
        )
        return item

    @staticmethod
    def listar(numero_avaliacao):
        return AvaliacaoServicoDAO.listar_servicos_da_avaliacao(numero_avaliacao)
