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
