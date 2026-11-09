
from datetime import datetime, timezone

import psycopg
from flask import Blueprint, jsonify

from db import conectar_banco

devolucoes_bp = Blueprint("devolucoes", __name__)


@devolucoes_bp.route(
    "/emprestimos/<int:emprestimo_id>/devolver",
    methods=["PATCH"]
)
def devolver_livro(emprestimo_id):

    if emprestimo_id < 1:
        return jsonify({
            "erro": "ID do emprestimo invalido."
        }), 400

    try:
        with conectar_banco() as conexao:
            with conexao.cursor() as cursor:

                agora = datetime.now(timezone.utc)

                cursor.execute(
                    """
                    UPDATE emprestimos
                    SET devolvido_em = %s
                    WHERE id = %s
                      AND devolvido_em IS NULL
                    RETURNING id, livro_id, leitor_id,
                              devolvido_em
                    """,
                    (agora, emprestimo_id)
                )

                resultado = cursor.fetchone()

                if resultado is None:
                    cursor.execute(
                        """
                        SELECT devolvido_em
                        FROM emprestimos
                        WHERE id = %s
                        """,
                        (emprestimo_id,)
                    )

                    emprestimo = cursor.fetchone()

                    if emprestimo is None:
                        return jsonify({
                            "erro": "Emprestimo nao encontrado."
                        }), 404

                    return jsonify({
                        "erro": "Este emprestimo ja foi devolvido."
                    }), 409

        return jsonify({
            "mensagem": "Livro devolvido com sucesso.",
            "emprestimo_id": resultado[0],
            "livro_id": resultado[1],
            "leitor_id": resultado[2],
            "devolvido_em": resultado[3].isoformat()
        }), 200

    except (psycopg.Error, RuntimeError):
        return jsonify({
            "erro": "Servico de dados indisponivel."
        }), 503
