from app.database import get_connection
from app.models.resposta import Resposta

class RespostaDAO:

    @staticmethod
    def inserir(resp: Resposta):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO resposta (numero_avaliacao, registro_servico, numero_questao,
                                  cpf_usuario, texto_resposta, codigo_opcao, valor_numerico)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING numero_resposta;
        """, (resp.numero_avaliacao, resp.registro_servico, resp.numero_questao,
              resp.cpf_usuario, resp.texto_resposta, resp.codigo_opcao, resp.valor_numerico))

        resp.numero_resposta = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return resp
