from app.database import get_connection
from app.models.servico import Servico
from app.models.avaliacao_servico import AvaliacaoServico

class AvaliacaoServicoDAO:

    @staticmethod
    def inserir(item: AvaliacaoServico):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO avaliacao_servico (numero_avaliacao, registro_servico)
            VALUES (%s, %s)
        """, (item.numero_avaliacao, item.registro_servico))

        conn.commit()
        cur.close()
        conn.close()
        return item

    @staticmethod
    def listar_servicos_da_avaliacao(numero_avaliacao):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT numero_avaliacao, registro_servico
            FROM avaliacao_servico
            WHERE numero_avaliacao = %s
        """, (numero_avaliacao,))

        rows = cur.fetchall()
        cur.close()
        conn.close()

        return [AvaliacaoServico(*row) for row in rows]

    @staticmethod
    def listar_por_avaliacao(numero_avaliacao):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT s.registro_servico, s.nome, s.descricao, s.endereco, s.codigo_bairro, s.sigla_secretaria
            FROM avaliacao_servico a
            JOIN servico s ON s.registro_servico = a.registro_servico
            WHERE a.numero_avaliacao = %s
            ORDER BY s.nome;
        """, (numero_avaliacao,))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        lista = []
        for row in rows:
            lista.append(Servico(*row))
        return lista
