from app.database import get_connection
from app.models.avaliacao import Avaliacao

class AvaliacaoDAO:

    @staticmethod
    def inserir(av: Avaliacao):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO avaliacao (titulo, descricao, data_inicio, data_fim, anonimato)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING numero_avaliacao;
        """, (av.titulo, av.descricao, av.data_inicio, av.data_fim, av.anonimato))
        
        av.numero_avaliacao = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return av

    @staticmethod
    def listar_todas():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT numero_avaliacao, titulo, descricao, data_inicio, data_fim, anonimato
            FROM avaliacao
            ORDER BY numero_avaliacao;
        """)

        rows = cur.fetchall()
        lista = []

        for r in rows:
            lista.append(Avaliacao(
                numero_avaliacao=r[0],
                titulo=r[1],
                descricao=r[2],
                data_inicio=r[3],
                data_fim=r[4],
                anonimato=r[5]
            ))

        cur.close()
        conn.close()
        return lista

    @staticmethod
    def buscar_por_id(id_avaliacao: int):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT numero_avaliacao, titulo, descricao, data_inicio, data_fim, anonimato
            FROM avaliacao
            WHERE numero_avaliacao = %s;
        """, (id_avaliacao,))

        r = cur.fetchone()

        cur.close()
        conn.close()

        if not r:
            return None

        return Avaliacao(
            numero_avaliacao=r[0],
            titulo=r[1],
            descricao=r[2],
            data_inicio=r[3],
            data_fim=r[4],
            anonimato=r[5]
        )

