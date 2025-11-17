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
