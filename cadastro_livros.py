
from flask import Blueprint, jsonify, request
from db import conectar_banco
import psycopg

cadastro_bp = Blueprint("cadastro", __name__)


@cadastro_bp.route("/livros", methods=["POST"])
def cadastrar_livro():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({
            "erro": "Envie um JSON valido."
        }), 400

    titulo = dados.get("titulo")
    autor = dados.get("autor")
    isbn = dados.get("isbn")
    exemplares = dados.get("exemplares")

    if not all(
        isinstance(valor, str) and valor.strip()
        for valor in (titulo, autor, isbn)
    ):
        return jsonify({
            "erro": "Titulo, autor e ISBN sao obrigatorios."
        }), 400

    titulo = titulo.strip()
    autor = autor.strip()
    isbn = isbn.strip()

    if len(titulo) > 200 or len(autor) > 150 or len(isbn) > 20:
        return jsonify({
            "erro": "Um dos campos ultrapassa o limite permitido."
        }), 400

    if type(exemplares) is not int or exemplares < 1:
        return jsonify({
            "erro": "Exemplares deve ser um inteiro maior ou igual a 1."
        }), 400

    try:
        with conectar_banco() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO livros (titulo, autor, isbn, exemplares)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                """, (titulo, autor, isbn, exemplares))

                livro_id = cursor.fetchone()[0]

        return jsonify({
            "mensagem": "Livro cadastrado com sucesso.",
            "id": livro_id,
            "titulo": titulo,
            "autor": autor,
            "isbn": isbn,
            "exemplares": exemplares
        }), 201

    except psycopg.errors.UniqueViolation:
        return jsonify({
            "erro": "Ja existe um livro com este ISBN."
        }), 409

    except (psycopg.Error, RuntimeError):
        return jsonify({
            "erro": "Servico de dados indisponivel."
        }), 503
