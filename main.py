from datetime import datetime, timedelta

from app.models.bairro import Bairro
from app.models.usuario import Usuario
from app.models.questao import Questao
from app.models.avaliacao import Avaliacao

from app.controllers.usuario_controller import UsuarioController
from app.controllers.questao_controller import QuestaoController
from app.controllers.avaliacao_controller import AvaliacaoController
from app.dao.bairro_dao import BairroDAO


def main():
    print("Iniciando testes do sistema.")

    # 1. Cadastro de bairro
    bairro = Bairro(nome="Centro")
    BairroDAO.inserir(bairro)
    print(f"Bairro criado. ID: {bairro.codigo_bairro}")

    # 2. Cadastro de usuário
    usuario = Usuario(
        cpf=33333333333,
        nome="João Almeida",
        email="joao.almeida@example.com",
        codigo_bairro=bairro.codigo_bairro
    )
    UsuarioController.cadastrar_usuario(usuario)
    print(f"Usuário cadastrado. CPF: {usuario.cpf}")

    # 3. Cadastro de questão
    questao = Questao(
        texto="Como você avalia a organização do local?",
        tipo="escala",
        valor_min=1,
        valor_max=5
    )
    QuestaoController.cadastrar_questao(questao)
    print(f"Questão cadastrada. ID: {questao.numero_questao}")

    # 4. Cadastro de avaliação
    avaliacao = Avaliacao(
        titulo="Avaliação de Teste",
        descricao="Teste de fluxo do sistema",
        data_inicio=datetime.now(),
        data_fim=datetime.now() + timedelta(days=3),
        anonimato=False
    )
    AvaliacaoController.criar_avaliacao(avaliacao)
    print(f"Avaliação criada. ID: {avaliacao.numero_avaliacao}")

    # 5. Registrar resposta
    AvaliacaoController.registrar_resposta(
        numero_avaliacao=avaliacao.numero_avaliacao,
        registro_servico=1,  
        numero_questao=questao.numero_questao,
        cpf_usuario=usuario.cpf,
        valor_numerico=5
    )
    print("Resposta registrada com sucesso.")

    print("Fluxo concluído.")


if __name__ == "__main__":
    main()
