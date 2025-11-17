from app.database import get_connection
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
