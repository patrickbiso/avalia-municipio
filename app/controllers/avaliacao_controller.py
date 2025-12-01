from app.dao.avaliacao_dao import AvaliacaoDAO
from app.dao.resposta_dao import RespostaDAO
from app.dao.avaliacao_questao_dao import AvaliacaoQuestaoDAO
from app.dao.avaliacao_servico_dao import AvaliacaoServicoDAO
from app.models.resposta import Resposta


class AvaliacaoController:


    @staticmethod
    def criar_avaliacao(av):
        return AvaliacaoDAO.inserir(av)

    @staticmethod
    def listar_todas():
        return AvaliacaoDAO.listar_todas()

    @staticmethod
    def buscar(id_avaliacao: int):
        return AvaliacaoDAO.buscar_por_id(id_avaliacao)

    @staticmethod
    def associar_questao(numero_avaliacao, numero_questao, ordem=1, peso=1):
        from app.models.avaliacao_questao import AvaliacaoQuestao
        obj = AvaliacaoQuestao(numero_avaliacao, numero_questao, ordem, peso)
        return AvaliacaoQuestaoDAO.inserir(obj)

    @staticmethod
    def listar_questoes(numero_avaliacao):
        return AvaliacaoQuestaoDAO.listar_questoes_da_avaliacao(numero_avaliacao)


    @staticmethod
    def associar_servico(numero_avaliacao, registro_servico):
        from app.models.avaliacao_servico import AvaliacaoServico
        item = AvaliacaoServico(numero_avaliacao, registro_servico)
        return AvaliacaoServicoDAO.inserir(item)

    @staticmethod
    def listar_servicos(numero_avaliacao):
        return AvaliacaoServicoDAO.listar_servicos_da_avaliacao(numero_avaliacao)


    @staticmethod
    def registrar_resposta(numero_avaliacao, registro_servico, numero_questao, cpf_usuario,
                           texto_resposta=None, codigo_opcao=None, valor_numerico=None):

        r = Resposta(
            numero_avaliacao=numero_avaliacao,
            registro_servico=registro_servico,
            numero_questao=numero_questao,
            cpf_usuario=cpf_usuario,
            texto_resposta=texto_resposta,
            codigo_opcao=codigo_opcao,
            valor_numerico=valor_numerico
        )

        return RespostaDAO.inserir(r)
