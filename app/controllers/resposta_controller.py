from app.dao.resposta_dao import RespostaDAO
from app.models.resposta import Resposta


class RespostaController:

    @staticmethod
    def registrar_resposta(r: Resposta):
        return RespostaDAO.inserir(r)
