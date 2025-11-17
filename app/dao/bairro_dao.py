from app.database import get_connection
from app.models.bairro import Bairro

class BairroDAO:

    @staticmethod
    def inserir(bairro: Bairro):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO bairro (nome) VALUES (%s) RETURNING codigo_bairro;
        """, (bairro.nome,))
        bairro.codigo_bairro = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return bairro
