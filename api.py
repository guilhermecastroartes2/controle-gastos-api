from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
import os

app = Flask(__name__)
CORS(app)

ARQUIVO = "dados.csv"
USUARIOS = "usuarios.csv"

# CRIAR ARQUIVOS SE NÃO EXISTIR
if not os.path.exists(ARQUIVO):
    with open(ARQUIVO, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["email", "data", "valor", "categoria", "tipo", "descricao"])

if not os.path.exists(USUARIOS):
    with open(USUARIOS, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["email", "senha"])


# 🔐 REGISTER
@app.route("/register", methods=["POST"])
def register():
    data = request.json

    with open(USUARIOS, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([data["email"], data["senha"]])

    return jsonify({"msg": "ok"})


# 🔐 LOGIN
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


# 📥 LISTAR
@app.route("/transacoes", methods=["GET"])
def listar():
    email = request.args.get("email")
    dados = []

    with open(ARQUIVO, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)

        for linha in reader:
            if linha[0] == email:
                dados.append({
                    "email": linha[0],
                    "data": linha[1],
                    "valor": linha[2],
                    "categoria": linha[3],
                    "tipo": linha[4],
                    "descricao": linha[5],
                })

    return jsonify(dados)


# ➕ ADICIONAR
@app.route("/transacoes", methods=["POST"])
def adicionar():
    data = request.json

    nova = [
        data["email"],
        "2026-01-01",
        data["valor"],
        data["categoria"],
        data["tipo"],
        data["descricao"],
    ]

    with open(ARQUIVO, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(nova)

    return jsonify({
        "email": data["email"],
        "data": "2026-01-01",
        "valor": data["valor"],
        "categoria": data["categoria"],
        "tipo": data["tipo"],
        "descricao": data["descricao"],
    })


app.run(host="0.0.0.0", port=5000)