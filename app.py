
from flask import Flask, jsonify
from datetime import datetime, timezone

app = Flask(__name__)

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
    return jsonify({
        "status": "api_iniciada",
        "iniciado_em": INICIADO_EM,
        "banco": "conexao_ainda_nao_implementada"
    }), 200


if __name__ == "__main__":
    app.run(debug=True)
