from app.dao.servico_dao import ServicoDAO

class ServicoController:

    @staticmethod
    def cadastrar_servico(servico):
        return ServicoDAO.inserir(servico)

    @staticmethod
    def buscar_servico(registro):
        return ServicoDAO.buscar_por_id(registro)
