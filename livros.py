
from flask import Blueprint, jsonify
from db import conectar_banco
import psycopg

livros_bp = Blueprint("livros", __name__)


@livros_bp.route("/livros", methods=["GET"])
def listar_livros():
    try:
        with conectar_banco() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    SELECT
                        l.id,
                        l.titulo,
                        l.autor,
                        l.isbn,
                        l.exemplares,
                        l.exemplares - COUNT(e.id)
                            FILTER (
                                WHERE e.devolvido_em IS NULL
                            ) AS disponiveis
                    FROM livros l
                    LEFT JOIN emprestimos e
                        ON e.livro_id = l.id
                    GROUP BY l.id
                    ORDER BY l.titulo
                """)

                colunas = [
                    coluna.name
                    for coluna in cursor.description
                ]

                livros = [
                    dict(zip(colunas, linha))
                    for linha in cursor.fetchall()
                ]

        return jsonify(livros), 200

    except (psycopg.Error, RuntimeError):
        return jsonify({
            "erro": "Servico de dados indisponivel"
        }), 503
