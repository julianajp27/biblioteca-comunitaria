
from flask import Blueprint, jsonify, request
from db import conectar_banco
import psycopg

livros_bp = Blueprint("livros", __name__)


@livros_bp.route("/livros", methods=["GET"])
def listar_livros():
    try:
        busca = request.args.get("busca", "").strip()

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
                    WHERE l.titulo ILIKE %s
                       OR l.autor ILIKE %s
                    GROUP BY l.id
                    ORDER BY l.titulo
                """, (f"%{busca}%", f"%{busca}%"))

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
