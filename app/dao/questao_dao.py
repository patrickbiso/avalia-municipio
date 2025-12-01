from app.database import get_connection
from app.models.questao import Questao

class QuestaoDAO:

    @staticmethod
    def inserir(questao: Questao):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO questao (texto, tipo, valor_min, valor_max, obrigatoria)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING numero_questao;
        """, (questao.texto, questao.tipo, questao.valor_min, questao.valor_max, questao.obrigatoria))
        
        questao.numero_questao = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return questao

    @staticmethod
    def listar_por_avaliacao(id_avaliacao: int):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT q.numero_questao, q.texto, q.tipo, q.valor_min, q.valor_max, q.obrigatoria
            FROM questao q
            JOIN avaliacao_questao aq ON aq.numero_questao = q.numero_questao
            WHERE aq.numero_avaliacao = %s
            ORDER BY q.numero_questao;
        """, (id_avaliacao,))

        rows = cur.fetchall()
        lista = []

        for r in rows:
            lista.append(Questao(
                numero_questao=r[0],
                texto=r[1],
                tipo=r[2],
                valor_min=r[3],
                valor_max=r[4],
                obrigatoria=r[5]
            ))

        cur.close()
        conn.close()
        return lista

    @staticmethod
    def listar_todas():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT numero_questao, texto, tipo, valor_min, valor_max, obrigatoria
            FROM questao
            ORDER BY numero_questao;
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        lista = []
        for row in rows:
            obj = Questao(*row)
            lista.append(obj)
        return lista
