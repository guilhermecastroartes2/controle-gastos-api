from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

ARQUIVO = "dados.csv"
USUARIOS = "usuarios.csv"

def inicializar_csv():
    if not os.path.exists(ARQUIVO):
        with open(ARQUIVO, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["email", "data", "valor", "categoria", "tipo", "descricao"])

    if not os.path.exists(USUARIOS):
        with open(USUARIOS, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["email", "senha"])

inicializar_csv()

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    with open(USUARIOS, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([data["email"], data["senha"]])
    return jsonify({"msg": "ok"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    with open(USUARIOS, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for linha in reader:
            if linha[0] == data["email"] and linha[1] == data["senha"]:
                return jsonify({"msg": "ok"})
    return jsonify({"erro": "login inválido"}), 401

@app.route("/transacoes", methods=["GET"])
def listar():
    email = request.args.get("email")
    dados = []
    if not os.path.exists(ARQUIVO): return jsonify([])

    with open(ARQUIVO, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)
        for linha in reader:
            if linha[0] == email:
                dados.append({
                    "email": linha[0], "data": linha[1], "valor": linha[2],
                    "categoria": linha[3], "tipo": linha[4], "descricao": linha[5],
                })
    return jsonify(dados)

@app.route("/transacoes", methods=["POST"])
def adicionar():
    data = request.json
    data_atual = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Salva no CSV
    nova_linha = [
        data["email"],
        data_atual,
        data["valor"],
        data["categoria"],
        data["tipo"],
        data["descricao"],
    ]

    with open(ARQUIVO, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(nova_linha)

    return jsonify({
        "email": data["email"],
        "data": data_atual,
        "valor": data["valor"],
        "categoria": data["categoria"],
        "tipo": data["tipo"],
        "descricao": data["descricao"],
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)