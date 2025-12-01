from app.dao.usuario_dao import UsuarioDAO


class UsuarioController:

    @staticmethod
    def cadastrar_usuario(usuario):
        return UsuarioDAO.inserir(usuario)

    @staticmethod
    def buscar_usuario(cpf):
        return UsuarioDAO.buscar_por_cpf(cpf)
