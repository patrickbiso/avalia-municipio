from app.database import get_connection
from app.models.secretaria import Secretaria

class SecretariaDAO:

    @staticmethod
    def inserir(secretaria: Secretaria):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO secretaria (nome, descricao)
            VALUES (%s, %s)
            RETURNING sigla_secretaria;
        """, (secretaria.nome, secretaria.descricao))

        secretaria.sigla_secretaria = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return secretaria

    @staticmethod
    def buscar_por_id(sigla):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT sigla_secretaria, nome, descricao FROM secretaria WHERE sigla_secretaria = %s", (sigla,))
        row = cur.fetchone()
        cur.close()
        conn.close()

        if not row:
            return None
        
        return Secretaria(sigla_secretaria=row[0], nome=row[1], descricao=row[2])
