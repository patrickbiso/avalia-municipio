from app.database import get_connection
from app.models.resposta import Resposta

class RespostaDAO:

    @staticmethod
    def inserir(resp: Resposta):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO resposta (
                numero_avaliacao,
                registro_servico,
                numero_questao,
                cpf_usuario,
                texto_resposta,
                codigo_opcao,
                valor_numerico
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING numero_resposta;
        """, (
            resp.numero_avaliacao,
            resp.registro_servico,
            resp.numero_questao,
            resp.cpf_usuario,
            resp.texto_resposta,
            resp.codigo_opcao,
            resp.valor_numerico
        ))

        resp.numero_resposta = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        return resp

    # ---------- RELATÓRIOS ----------

    @staticmethod
    def media_por_servico(limit=None):
        """
        Retorna lista de dicts: [{ 'registro_servico': int, 'nome': str, 'media': float }, ...]
        """
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT s.registro_servico, s.nome, AVG(r.valor_numerico) AS media
            FROM resposta r
            JOIN servico s ON s.registro_servico = r.registro_servico
            GROUP BY s.registro_servico, s.nome
            HAVING AVG(r.valor_numerico) IS NOT NULL
            ORDER BY media DESC;
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        result = []
        for r in rows:
            result.append({
                "registro_servico": r[0],
                "nome": r[1],
                "media": float(r[2]) if r[2] is not None else None
            })
        if limit:
            return result[:limit]
        return result

    @staticmethod
    def media_por_secretaria():
        """
        Média agregada por secretaria (usando sigla_secretaria da tabela servico).
        Retorna list of dicts: [{ 'sigla': str, 'media': float, 'count_servicos': int }, ...]
        """
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT s.sigla_secretaria, AVG(r.valor_numerico) AS media, COUNT(DISTINCT s.registro_servico) as qtd_servicos
            FROM resposta r
            JOIN servico s ON s.registro_servico = r.registro_servico
            GROUP BY s.sigla_secretaria
            HAVING AVG(r.valor_numerico) IS NOT NULL
            ORDER BY media DESC;
        """)
        rows = cur.fetchall()
        cur.close()
        conn.close()

        result = []
        for r in rows:
            result.append({
                "sigla": r[0],
                "media": float(r[1]) if r[1] is not None else None,
                "qtd_servicos": int(r[2])
            })
        return result

    @staticmethod
    def evolucao_mensal(numero_avaliacao=None, registro_servico=None):
        """
        Evolução média mensal.
        Se passar numero_avaliacao ou registro_servico, filtra por eles.
        Retorna list of dicts: [{ 'ano_mes': 'YYYY-MM', 'media': float }, ...] ordenado asc.
        """
        conn = get_connection()
        cur = conn.cursor()

        # constrói filtro dinâmico
        filters = []
        params = []
        if numero_avaliacao:
            filters.append("r.numero_avaliacao = %s")
            params.append(numero_avaliacao)
        if registro_servico:
            filters.append("r.registro_servico = %s")
            params.append(registro_servico)

        where = "WHERE " + " AND ".join(filters) if filters else ""

        query = f"""
            SELECT to_char(date_trunc('month', r.criado_em), 'YYYY-MM') as ano_mes,
                   AVG(r.valor_numerico) as media
            FROM resposta r
            {where}
            GROUP BY ano_mes
            ORDER BY ano_mes;
        """
        cur.execute(query, tuple(params))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        result = []
        for r in rows:
            result.append({"ano_mes": r[0], "media": float(r[1]) if r[1] is not None else None})
        return result

    @staticmethod
    def distribuicao_por_questao(numero_avaliacao, numero_questao):
        """
        Retorna contagem de respostas por valor (1..5) para a questão dentro de uma avaliação.
        Saída: dict {1: count, 2: count, ..., 5: count}
        Se faltarem valores, retorna 0.
        """
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT r.valor_numerico, COUNT(*) 
            FROM resposta r
            WHERE r.numero_avaliacao = %s AND r.numero_questao = %s
            GROUP BY r.valor_numerico;
        """, (numero_avaliacao, numero_questao))
        rows = cur.fetchall()
        cur.close()
        conn.close()

        counts = {i: 0 for i in range(1, 6)}
        for val, cnt in rows:
            try:
                k = int(val)
                if 1 <= k <=5:
                    counts[k] = cnt
            except:
                continue
        return counts
