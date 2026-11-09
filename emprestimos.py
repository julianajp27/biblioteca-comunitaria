
from datetime import datetime, timedelta, timezone

import psycopg
from flask import Blueprint, jsonify, request

from db import conectar_banco

emprestimos_bp = Blueprint("emprestimos", __name__)


@emprestimos_bp.route("/emprestimos", methods=["POST"])
def registrar_emprestimo():
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({
            "erro": "Envie um JSON valido."
        }), 400

    livro_id = dados.get("livro_id")
    leitor_id = dados.get("leitor_id")

    if (
        type(livro_id) is not int or livro_id < 1
        or type(leitor_id) is not int or leitor_id < 1
    ):
        return jsonify({
            "erro": "livro_id e leitor_id devem ser inteiros positivos."
        }), 400

    try:
        with conectar_banco() as conexao:
            with conexao.cursor() as cursor:

                # Bloqueia o registro do leitor para evitar
                # emprestimos simultaneos acima do limite.
                cursor.execute(
                    "SELECT id FROM leitores WHERE id = %s FOR UPDATE",
                    (leitor_id,)
                )

                if cursor.fetchone() is None:
                    return jsonify({
                        "erro": "Leitor nao encontrado."
                    }), 404

                # Bloqueia o livro durante a verificacao
                # da disponibilidade.
                cursor.execute(
                    """
                    SELECT exemplares
                    FROM livros
                    WHERE id = %s
                    FOR UPDATE
                    """,
                    (livro_id,)
                )

                resultado = cursor.fetchone()

                if resultado is None:
                    return jsonify({
                        "erro": "Livro nao encontrado."
                    }), 404

                total_exemplares = resultado[0]

                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM emprestimos
                    WHERE leitor_id = %s
                      AND devolvido_em IS NULL
                    """,
                    (leitor_id,)
                )

                ativos_leitor = cursor.fetchone()[0]

                if ativos_leitor >= 2:
                    return jsonify({
                        "erro": "Leitor ja possui 2 emprestimos ativos."
                    }), 409

                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM emprestimos
                    WHERE livro_id = %s
                      AND devolvido_em IS NULL
                    """,
                    (livro_id,)
                )

                ativos_livro = cursor.fetchone()[0]

                if ativos_livro >= total_exemplares:
                    return jsonify({
                        "erro": "Nao ha exemplares disponiveis."
                    }), 409

                agora = datetime.now(timezone.utc)
                previsto = agora + timedelta(days=14)

                cursor.execute(
                    """
                    INSERT INTO emprestimos (
                        livro_id,
                        leitor_id,
                        emprestado_em,
                        previsto_para
                    )
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                    """,
                    (livro_id, leitor_id, agora, previsto)
                )

                emprestimo_id = cursor.fetchone()[0]

        return jsonify({
            "mensagem": "Emprestimo registrado com sucesso.",
            "id": emprestimo_id,
            "livro_id": livro_id,
            "leitor_id": leitor_id,
            "emprestado_em": agora.isoformat(),
            "previsto_para": previsto.isoformat()
        }), 201

    except (psycopg.Error, RuntimeError):
        return jsonify({
            "erro": "Servico de dados indisponivel."
        }), 503
