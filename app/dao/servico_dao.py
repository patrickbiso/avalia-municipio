from app.database import get_connection
from app.models.servico import Servico


class ServicoDAO:

    @staticmethod
    def inserir(servico: Servico):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO servico (nome, descricao, endereco, codigo_bairro, sigla_secretaria)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING registro_servico;
        """, (
            servico.nome,
            servico.descricao,
            servico.endereco,
            servico.codigo_bairro,
            servico.sigla_secretaria,
        ))

        servico.registro_servico = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return servico

    @staticmethod
    def buscar_por_id(registro):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT registro_servico, nome, descricao, endereco, codigo_bairro, sigla_secretaria
            FROM servico
            WHERE registro_servico = %s
        """, (registro,))

        row = cur.fetchone()
        cur.close()
        conn.close()

        if not row:
            return None

        return Servico(*row)

    @staticmethod
    def listar_por_avaliacao(id_avaliacao: int):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT s.registro_servico, s.nome, s.descricao, s.endereco, s.codigo_bairro, s.sigla_secretaria
            FROM servico s
            JOIN avaliacao_servico avs ON avs.registro_servico = s.registro_servico
            WHERE avs.numero_avaliacao = %s
            ORDER BY s.registro_servico;
        """, (id_avaliacao,))

        rows = cur.fetchall()
        cur.close()
        conn.close()

        lista = []
        for r in rows:
            lista.append(Servico(
                registro_servico=r[0],
                nome=r[1],
                descricao=r[2],
                endereco=r[3],
                codigo_bairro=r[4],
                sigla_secretaria=r[5]
            ))

        return lista

    @staticmethod
    def listar_todos():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT registro_servico, nome, descricao, endereco, codigo_bairro, sigla_secretaria
            FROM servico
            ORDER BY nome;
        """)

        rows = cur.fetchall()
        cur.close()
        conn.close()

        lista = []
        for r in rows:
            lista.append(Servico(*r))

        return lista
