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
