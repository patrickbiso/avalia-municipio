from app.database import get_connection
from app.models.opcao import Opcao

class OpcaoDAO:

    @staticmethod
    def inserir(op: Opcao):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO opcao (letra, texto, valor_numerico, numero_questao)
            VALUES (%s, %s, %s, %s)
            RETURNING codigo_opcao;
        """, (op.letra, op.texto, op.valor_numerico, op.numero_questao))

        op.codigo_opcao = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return op

    @staticmethod
    def listar_por_questao(numero_questao):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT codigo_opcao, letra, texto, valor_numerico, numero_questao
            FROM opcao WHERE numero_questao = %s
        """, (numero_questao,))

        rows = cur.fetchall()
        cur.close()
        conn.close()

        return [Opcao(*row) for row in rows]
