
from datetime import datetime, timezone

from flask import Flask, jsonify

from db import verificar_conexao
from livros import livros_bp
from cadastro_livros import cadastro_bp
from emprestimos import emprestimos_bp
from devolucoes import devolucoes_bp
from atrasados import atrasados_bp

app = Flask(__name__)

# Registro das rotas da API
app.register_blueprint(livros_bp)
app.register_blueprint(cadastro_bp)
app.register_blueprint(emprestimos_bp)
app.register_blueprint(devolucoes_bp)
app.register_blueprint(atrasados_bp)

# Data e hora de inicializacao
INICIADO_EM = datetime.now(timezone.utc).isoformat()


@app.route("/", methods=["GET"])
def inicio():
    return jsonify({
        "projeto": "Biblioteca Comunitaria",
        "desafio": "Cloud Challenge 06",
        "status": "API em desenvolvimento",
        "rotas": {
            "saude": "GET /health",
            "listar_livros": "GET /livros",
            "buscar_livros": "GET /livros?busca=termo",
            "cadastrar_livro": "POST /livros",
            "registrar_emprestimo": "POST /emprestimos",
            "devolver_livro": "PATCH /emprestimos/<id>/devolver",
            "listar_atrasados": "GET /emprestimos/atrasados"
        }
    }), 200


@app.route("/health", methods=["GET"])
def health():
    if verificar_conexao():
        return jsonify({
            "status": "ok",
            "banco": "conectado",
            "iniciado_em": INICIADO_EM
        }), 200

    return jsonify({
        "status": "indisponivel",
        "banco": "sem_conexao",
        "iniciado_em": INICIADO_EM
    }), 503


if __name__ == "__main__":
    app.run(debug=True)
