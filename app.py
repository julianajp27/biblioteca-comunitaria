
from flask import Flask, jsonify
from datetime import datetime, timezone
from db import verificar_conexao
from livros import livros_bp

app = Flask(__name__)
app.register_blueprint(livros_bp)

INICIADO_EM = datetime.now(timezone.utc).isoformat()


@app.route("/")
def inicio():
    return jsonify({
        "projeto": "Biblioteca Comunitária",
        "desafio": "Cloud Challenge 06",
        "status": "API em desenvolvimento"
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
