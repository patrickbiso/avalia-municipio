from app.database import get_connection
from app.models.questao import Questao
from app.models.avaliacao_questao import AvaliacaoQuestao

class AvaliacaoQuestaoDAO:

    @staticmethod
    def inserir(item: AvaliacaoQuestao):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO avaliacao_questao (numero_avaliacao, numero_questao, ordem, peso)
            VALUES (%s, %s, %s, %s)
        """, (item.numero_avaliacao, item.numero_questao, item.ordem, item.peso))

        conn.commit()
        cur.close()
        conn.close()
        return item

    @staticmethod
    def listar_questoes_da_avaliacao(numero_avaliacao):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT numero_avaliacao, numero_questao, ordem, peso
            FROM avaliacao_questao
            WHERE numero_avaliacao = %s
            ORDER BY ordem ASC
        """, (numero_avaliacao,))

        rows = cur.fetchall()
        cur.close()
        conn.close()

        return [AvaliacaoQuestao(*row) for row in rows]
    
    @staticmethod
    def listar_por_avaliacao(numero_avaliacao):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT q.numero_questao, q.texto, q.tipo, q.valor_min, q.valor_max, q.obrigatoria
            FROM avaliacao_questao aq
            JOIN questao q ON q.numero_questao = aq.numero_questao
            WHERE aq.numero_avaliacao = %s
            ORDER BY aq.ordem;
        """, (numero_avaliacao,))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        lista = []
        for row in rows:
            lista.append(Questao(*row))
        return lista
