from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.dao.avaliacao_dao import AvaliacaoDAO
from app.dao.resposta_dao import RespostaDAO
from app.dao.questao_dao import QuestaoDAO
from app.dao.servico_dao import ServicoDAO
from app.dao.secretaria_dao import SecretariaDAO
from app.dao.avaliacao_questao_dao import AvaliacaoQuestaoDAO
from app.dao.avaliacao_servico_dao import AvaliacaoServicoDAO

from app.controllers.usuario_controller import UsuarioController
from app.controllers.avaliacao_controller import AvaliacaoController
from app.controllers.servico_controller import ServicoController
from app.controllers.secretaria_controller import SecretariaController
from app.controllers.questao_controller import QuestaoController
from app.controllers.avaliacao_questao_controller import AvaliacaoQuestaoController
from app.controllers.avaliacao_servico_controller import AvaliacaoServicoController
from app.controllers.relatorio_controller import RelatorioController


app = Flask(__name__)
app.secret_key = "admin123"


@app.route("/")
def index():
    avaliacoes = AvaliacaoDAO.listar_todas()
    return render_template("index.html", avaliacoes=avaliacoes)


@app.route("/avaliacao/<int:id>", methods=["GET", "POST"])
def avaliacao(id):
    if request.method == "POST":
        cpf = request.form.get("cpf")
        numero_questao = int(request.form["questao"])
        registro_servico = int(request.form["servico"])
        valor = int(request.form["valor"])

        # Cria usuário se não existir
        UsuarioController.cadastrar_usuario(
            usuario=type("usr", (), {
                "cpf": cpf,
                "nome": "Visitante",
                "email": None,
                "codigo_bairro": None
            })
        )

        AvaliacaoController.registrar_resposta(
            numero_avaliacao=id,
            registro_servico=registro_servico,
            numero_questao=numero_questao,
            cpf_usuario=cpf,
            valor_numerico=valor
        )

        return redirect(url_for("index"))

    questoes = QuestaoDAO.listar_por_avaliacao(id)
    servicos = ServicoDAO.listar_por_avaliacao(id)

    return render_template("avaliacao.html", questoes=questoes, servicos=servicos, id=id)


@app.route("/relatorios")
def relatorios():
    ranking = RelatorioController.ranking_servicos(top_n=10)
    media_secretarias = RelatorioController.media_secretarias()
    evolucao = RelatorioController.evolucao_mensal()

    return render_template(
        "relatorios.html",
        ranking_json=ranking,
        secretaria_json=media_secretarias,
        evolucao_json=evolucao
    )


@app.route("/relatorios/distribuicao")
def relatorios_distribuicao():
    numero_avaliacao = int(request.args.get("numero_avaliacao"))
    numero_questao = int(request.args.get("numero_questao"))

    dados = RelatorioController.distribuicao(numero_avaliacao, numero_questao)
    return jsonify({"counts": dados})


def admin_required():
    if "admin" not in session:
        return redirect("/admin/login")


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        user = request.form["user"]
        senha = request.form["senha"]

        if user == "admin" and senha == "123":
            session["admin"] = True
            return redirect("/admin")

        return render_template("admin/login.html", erro="Credenciais inválidas")

    return render_template("admin/login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect("/admin/login")

@app.route("/admin")
def admin_dashboard():
    if "admin" not in session:
        return redirect("/admin/login")
    return render_template("admin/dashboard.html")

@app.route("/admin/secretarias", methods=["GET", "POST"])
def admin_secretarias():
    if "admin" not in session:
        return redirect("/admin/login")

    if request.method == "POST":
        sigla = request.form["sigla"]
        nome = request.form["nome"]
        SecretariaController.cadastrar_secretaria(
            type("sec", (), {"sigla": sigla, "nome": nome})
        )

    secretarias = SecretariaDAO.listar_todas()
    return render_template("admin/secretarias.html", secretarias=secretarias)

@app.route("/admin/servicos")
def admin_servicos():
    if "admin" not in session:
        return redirect("/admin/login")
    servicos = ServicoDAO.listar_todos()
    return render_template("admin/servicos.html", servicos=servicos)


@app.route("/admin/servicos/novo", methods=["GET", "POST"])
def admin_servicos_novo():
    if "admin" not in session:
        return redirect("/admin/login")

    secretarias = SecretariaDAO.listar_todas()

    if request.method == "POST":
        nome = request.form["nome"]
        descricao = request.form["descricao"]
        sigla = request.form["sigla_secretaria"]

        s = type("s", (), {
            "nome": nome,
            "descricao": descricao,
            "endereco": None,
            "codigo_bairro": None,
            "sigla_secretaria": sigla
        })

        ServicoController.cadastrar_servico(s)
        return redirect("/admin/servicos")

    return render_template("admin/servico_edit.html", servico=None, secretarias=secretarias)


@app.route("/admin/servicos/<int:id>", methods=["GET", "POST"])
def admin_servicos_editar(id):
    if "admin" not in session:
        return redirect("/admin/login")

    servico = ServicoDAO.buscar_por_id(id)
    secretarias = SecretariaDAO.listar_todas()

    if request.method == "POST":
        servico.nome = request.form["nome"]
        servico.descricao = request.form["descricao"]
        servico.sigla_secretaria = request.form["sigla_secretaria"]

        ServicoDAO.atualizar(servico)
        return redirect("/admin/servicos")

    return render_template("admin/servico_edit.html", servico=servico, secretarias=secretarias)

@app.route("/admin/questoes")
def admin_questoes():
    if "admin" not in session:
        return redirect("/admin/login")

    questoes = QuestaoDAO.listar_todas()
    return render_template("admin/questoes.html", questoes=questoes)


@app.route("/admin/questoes/novo", methods=["GET", "POST"])
def admin_questoes_novo():
    if "admin" not in session:
        return redirect("/admin/login")

    if request.method == "POST":
        texto = request.form["texto"]
        tipo = request.form["tipo"]

        q = type("q", (), {
            "texto": texto,
            "tipo": tipo,
            "valor_min": 1,
            "valor_max": 5,
            "obrigatoria": True
        })

        QuestaoController.cadastrar_questao(q)
        return redirect("/admin/questoes")

    return render_template("admin/questao_edit.html", questao=None)


@app.route("/admin/questoes/<int:id>", methods=["GET", "POST"])
def admin_questoes_editar(id):
    if "admin" not in session:
        return redirect("/admin/login")

    todas = QuestaoDAO.listar_todas()
    questao = next((q for q in todas if q.numero_questao == id), None)

    if request.method == "POST":
        questao.texto = request.form["texto"]
        QuestaoDAO.atualizar(questao)
        return redirect("/admin/questoes")

    return render_template("admin/questao_edit.html", questao=questao)

@app.route("/admin/avaliacoes")
def admin_avaliacoes():
    if "admin" not in session:
        return redirect("/admin/login")
    avaliacoes = AvaliacaoDAO.listar_todas()
    return render_template("admin/avaliacoes.html", avaliacoes=avaliacoes)


@app.route("/admin/avaliacoes/nova", methods=["GET", "POST"])
def admin_avaliacoes_nova():
    if "admin" not in session:
        return redirect("/admin/login")

    if request.method == "POST":
        titulo = request.form["titulo"]
        descricao = request.form["descricao"]

        a = type("a", (), {
            "titulo": titulo,
            "descricao": descricao,
            "data_inicio": None,
            "data_fim": None,
            "anonimato": False
        })

        AvaliacaoController.criar_avaliacao(a)
        return redirect("/admin/avaliacoes")

    return render_template("admin/avaliacao_edit.html", avaliacao=None)


@app.route("/admin/avaliacoes/<int:id>", methods=["GET", "POST"])
def admin_avaliacoes_editar(id):
    if "admin" not in session:
        return redirect("/admin/login")

    avaliacao = AvaliacaoDAO.buscar_por_id(id)
    todas_questoes = QuestaoDAO.listar_todas()
    todos_servicos = ServicoDAO.listar_todos()
    questoes = QuestaoDAO.listar_por_avaliacao(id)
    servicos = ServicoDAO.listar_por_avaliacao(id)

    if request.method == "POST":
        avaliacao.titulo = request.form["titulo"]
        avaliacao.descricao = request.form["descricao"]
        AvaliacaoDAO.atualizar(avaliacao)

    return render_template(
        "admin/avaliacao_edit.html",
        avaliacao=avaliacao,
        todas_questoes=todas_questoes,
        todos_servicos=todos_servicos,
        questoes=questoes,
        servicos=servicos
    )


@app.route("/admin/avaliacoes/<int:id>/add_questao", methods=["POST"])
def admin_avaliacoes_add_questao(id):
    numero_questao = int(request.form["numero_questao"])
    AvaliacaoQuestaoController.adicionar_questao(id, numero_questao)
    return redirect(f"/admin/avaliacoes/{id}")


@app.route("/admin/avaliacoes/<int:id>/add_servico", methods=["POST"])
def admin_avaliacoes_add_servico(id):
    registro_servico = int(request.form["registro_servico"])
    AvaliacaoServicoController.adicionar_servico(id, registro_servico)
    return redirect(f"/admin/avaliacoes/{id}")

if __name__ == "__main__":
    app.run(debug=True)
