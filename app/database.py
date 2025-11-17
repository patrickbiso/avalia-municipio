import psycopg2

def get_connection():
    conn = psycopg2.connect(
        dbname="avaliacao_db",
        user="postgres",
        password="123456",
        host="localhost",
        port="5432"
    )

    
    cur = conn.cursor()
    cur.execute("SET search_path TO avaliacao, public;")
    cur.close()

    return conn