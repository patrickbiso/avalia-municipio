from app.dao.secretaria_dao import SecretariaDAO


class SecretariaController:

    @staticmethod
    def cadastrar_secretaria(sec):
        return SecretariaDAO.inserir(sec)

    @staticmethod
    def buscar_secretaria(sigla):
        return SecretariaDAO.buscar_por_id(sigla)

    @staticmethod
    def listar_secretarias():
        return SecretariaDAO.listar_todas()
