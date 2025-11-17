from app.dao.questao_dao import QuestaoDAO
from app.dao.opcao_dao import OpcaoDAO

class QuestaoController:

    @staticmethod
    def cadastrar_questao(questao, opcoes=None):
        questao = QuestaoDAO.inserir(questao)

        if opcoes:
            for op in opcoes:
                op.numero_questao = questao.numero_questao
                OpcaoDAO.inserir(op)

        return questao

    @staticmethod
    def listar_opcoes(numero_questao):
        return OpcaoDAO.listar_por_questao(numero_questao)
