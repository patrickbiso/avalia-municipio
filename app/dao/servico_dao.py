from app.database import get_connection
from app.models.servico import Servico

class ServicoDAO:

    @staticmethod
    def inserir(servico: Servico):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO servico (nome, descricao, endereco, codigo_bairro, sigla_secretaria)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING registro_servico;
        """, (
            servico.nome,
            servico.descricao,
            servico.endereco,
            servico.codigo_bairro,
            servico.sigla_secretaria,
        ))

        servico.registro_servico = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return servico

    @staticmethod
    def buscar_por_id(registro):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT registro_servico, nome, descricao, endereco, codigo_bairro, sigla_secretaria
            FROM servico WHERE registro_servico = %s
        """, (registro,))
        row = cur.fetchone()
        cur.close()
        conn.close()

        if not row:
            return None
        
        return Servico(*row)
