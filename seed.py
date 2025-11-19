from datetime import datetime, timedelta

from app.models.bairro import Bairro
from app.models.usuario import Usuario
from app.models.secretaria import Secretaria
from app.models.servico import Servico
from app.models.questao import Questao
from app.models.opcao import Opcao
from app.models.avaliacao import Avaliacao
from app.models.avaliacao_servico import AvaliacaoServico
from app.models.avaliacao_questao import AvaliacaoQuestao
from app.models.resposta import Resposta

from app.dao.bairro_dao import BairroDAO
from app.dao.usuario_dao import UsuarioDAO
from app.dao.secretaria_dao import SecretariaDAO
from app.dao.servico_dao import ServicoDAO
from app.dao.questao_dao import QuestaoDAO
from app.dao.opcao_dao import OpcaoDAO
from app.dao.avaliacao_dao import AvaliacaoDAO
from app.dao.avaliacao_servico_dao import AvaliacaoServicoDAO
from app.dao.avaliacao_questao_dao import AvaliacaoQuestaoDAO
from app.dao.resposta_dao import RespostaDAO


def seed():
    print("\n=== Iniciando Seed ===\n")

    # 1. Bairros
    b1 = Bairro(nome="Centro")
    b2 = Bairro(nome="Jardins")
    BairroDAO.inserir(b1)
    BairroDAO.inserir(b2)

    # 2. Secretarias
    s1 = Secretaria(nome="Saúde", descricao="Serviços de saúde pública")
    s2 = Secretaria(nome="Educação", descricao="Escolas municipais")
    SecretariaDAO.inserir(s1)
    SecretariaDAO.inserir(s2)

    # 3. Serviços
    serv1 = Servico(
        nome="UBS Central",
        descricao="Unidade Básica de Saúde",
        endereco="Rua Central, 100",
        codigo_bairro=b1.codigo_bairro,
        sigla_secretaria=s1.sigla_secretaria
    )

    serv2 = Servico(
        nome="UBS Jardins",
        descricao="UBS do bairro Jardins",
        endereco="Av. Jardins, 200",
        codigo_bairro=b2.codigo_bairro,
        sigla_secretaria=s1.sigla_secretaria
    )

    serv3 = Servico(
        nome="Escola Municipal Alfa",
        descricao="Ensino Fundamental",
        endereco="Rua Alfa, 321",
        codigo_bairro=b1.codigo_bairro,
        sigla_secretaria=s2.sigla_secretaria
    )

    ServicoDAO.inserir(serv1)
    ServicoDAO.inserir(serv2)
    ServicoDAO.inserir(serv3)

    # 4. Questões
    q1 = Questao(
        texto="Como você avalia o atendimento?",
        tipo="escala",
        valor_min=1,
        valor_max=5
    )
    QuestaoDAO.inserir(q1)

    q2 = Questao(
        texto="Qual foi o tempo de espera?",
        tipo="multipla"
    )
    QuestaoDAO.inserir(q2)

    # 5. Opções da questão múltipla
    OpcaoDAO.inserir(Opcao(letra="A", texto="Menos de 10 minutos", valor_numerico=5, numero_questao=q2.numero_questao))
    OpcaoDAO.inserir(Opcao(letra="B", texto="10 a 30 minutos", valor_numerico=3, numero_questao=q2.numero_questao))
    OpcaoDAO.inserir(Opcao(letra="C", texto="Mais de 30 minutos", valor_numerico=1, numero_questao=q2.numero_questao))

    # 6. Avaliação
    avaliacao = Avaliacao(
        titulo="Pesquisa de Satisfação - Saúde",
        descricao="Avaliação dos serviços de saúde",
        data_inicio=datetime.now(),
        data_fim=datetime.now() + timedelta(days=5),
        anonimato=False
    )
    AvaliacaoDAO.inserir(avaliacao)

    # 7. Associação avaliação x questões
    AvaliacaoQuestaoDAO.inserir(AvaliacaoQuestao(avaliacao.numero_avaliacao, q1.numero_questao, ordem=1))
    AvaliacaoQuestaoDAO.inserir(AvaliacaoQuestao(avaliacao.numero_avaliacao, q2.numero_questao, ordem=2))

    # 8. Associação avaliação x serviços
    AvaliacaoServicoDAO.inserir(AvaliacaoServico(avaliacao.numero_avaliacao, serv1.registro_servico))
    AvaliacaoServicoDAO.inserir(AvaliacaoServico(avaliacao.numero_avaliacao, serv2.registro_servico))

    # 9. Usuários
    u1 = Usuario(cpf=11111111111, nome="Maria Oliveira", email="maria@gmail.com", codigo_bairro=b1.codigo_bairro)
    u2 = Usuario(cpf=22222222222, nome="Carlos Souza", email="carlos@gmail.com", codigo_bairro=b2.codigo_bairro)
    UsuarioDAO.inserir(u1)
    UsuarioDAO.inserir(u2)

    # 10. Respostas de exemplo
    RespostaDAO.inserir(Resposta(
        numero_avaliacao=avaliacao.numero_avaliacao,
        registro_servico=serv1.registro_servico,
        numero_questao=q1.numero_questao,
        cpf_usuario=u1.cpf,
        valor_numerico=4
    ))

    RespostaDAO.inserir(Resposta(
        numero_avaliacao=avaliacao.numero_avaliacao,
        registro_servico=serv1.registro_servico,
        numero_questao=q2.numero_questao,
        cpf_usuario=u1.cpf,
        codigo_opcao=1  
    ))

    print("\n=== Seed concluído ===\n")


if __name__ == "__main__":
    seed()
