
from datetime import datetime, timezone

import psycopg
from flask import Blueprint, jsonify

from db import conectar_banco

atrasados_bp = Blueprint("atrasados", __name__)


@atrasados_bp.route("/emprestimos/atrasados", methods=["GET"])
def listar_atrasados():
    try:
        with conectar_banco() as conexao:
            with conexao.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        e.id,
                        l.titulo,
                        l.autor,
                        r.nome AS leitor,
                        e.emprestado_em,
                        e.previsto_para
                    FROM emprestimos e
                    INNER JOIN livros l
                        ON e.livro_id = l.id
                    INNER JOIN leitores r
                        ON e.leitor_id = r.id
                    WHERE e.devolvido_em IS NULL
                      AND e.previsto_para < %s
                    ORDER BY e.previsto_para ASC
                    """,
                    (datetime.now(timezone.utc),)
                )

                colunas = [
                    coluna.name
                    for coluna in cursor.description
                ]

                registros = [
                    dict(zip(colunas, linha))
                    for linha in cursor.fetchall()
                ]

        # Converte datas para formato JSON
        for registro in registros:
            registro["emprestado_em"] = (
                registro["emprestado_em"].isoformat()
            )
            registro["previsto_para"] = (
                registro["previsto_para"].isoformat()
            )

        return jsonify({
            "total": len(registros),
            "emprestimos_atrasados": registros
        }), 200

    except (psycopg.Error, RuntimeError):
        return jsonify({
            "erro": "Servico de dados indisponivel."
        }), 503
