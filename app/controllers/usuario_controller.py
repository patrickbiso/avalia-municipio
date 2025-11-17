from app.dao.usuario_dao import UsuarioDAO

class UsuarioController:

    @staticmethod
    def cadastrar_usuario(usuario):
        return UsuarioDAO.inserir(usuario)
