from app.database import get_connection
from app.models.usuario import Usuario


class UsuarioDAO:

    @staticmethod
    def inserir(usuario: Usuario):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO usuario (cpf, nome, email, codigo_bairro)
            VALUES (%s, %s, %s, %s)
            RETURNING cpf;
        """, (usuario.cpf, usuario.nome, usuario.email, usuario.codigo_bairro))

        conn.commit()
        cur.close()
        conn.close()
        return usuario

    @staticmethod
    def buscar_por_cpf(cpf: int):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT cpf, nome, email, codigo_bairro
            FROM usuario
            WHERE cpf = %s
        """, (cpf,))

        row = cur.fetchone()
        cur.close()
        conn.close()

        if not row:
            return None

        return Usuario(
            cpf=row[0],
            nome=row[1],
            email=row[2],
            codigo_bairro=row[3]
        )

    @staticmethod
    def inserir_minimo(cpf: int):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO usuario (cpf, nome)
            VALUES (%s, %s)
        """, (cpf, "Anônimo"))

        conn.commit()
        cur.close()
        conn.close()
