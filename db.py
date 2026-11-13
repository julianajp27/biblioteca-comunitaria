import os
import psycopg
from dotenv import load_dotenv

load_dotenv()

def conectar_banco():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise RuntimeError("Variavel DATABASE_URL nao configurada")

    return psycopg.connect(database_url)

def verificar_conexao():
    try:
        with conectar_banco() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute("SELECT 1")
                cursor.fetchone()
        return True
    except Exception as e:
        print(f"=== ERRO DETALHADO DE CONEXAO ===: {e}")
        return False