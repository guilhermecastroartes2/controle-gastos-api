from flask import Flask, request, jsonify
from flask_cors import CORS
import csv
from datetime import datetime

app = Flask(__name__)
CORS(app)

ARQUIVO = "dados.csv"
ARQUIVO_USUARIOS = "usuarios.csv"
FORMATO_DATA = "%Y-%m-%d"

# =========================
# CADASTRO
# =========================
@app.route('/register', methods=['POST'])
def register():
    dados = request.json

    with open(ARQUIVO_USUARIOS, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([dados['email'], dados['senha']])

    return jsonify({"msg": "Usuário criado"})


# =========================
# LOGIN
# =========================
@app.route('/login', methods=['POST'])
def login():
    dados = request.json

    try:
        with open(ARQUIVO_USUARIOS, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)

            for linha in reader:
                if linha[0] == dados['email'] and linha[1] == dados['senha']:
                    return jsonify({"msg": "Login sucesso"})
    except:
        pass

    return jsonify({"erro": "Credenciais inválidas"}), 401


# =========================
# LISTAR TRANSAÇÕES (POR USUÁRIO)
# =========================
@app.route('/transacoes', methods=['GET'])
def listar_transacoes():
    usuario = request.args.get('usuario')
    dados = []

    try:
        with open(ARQUIVO, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)

            for linha in reader:
                if len(linha) < 6:
                    continue

                if linha[0] != usuario:
                    continue

                dados.append({
                    "data": linha[1],
                    "valor": linha[2],
                    "categoria": linha[3],
                    "tipo": linha[4],
                    "descricao": linha[5]
                })

    except:
        pass

    return jsonify(dados)


# =========================
# ADICIONAR TRANSAÇÃO
# =========================
@app.route('/transacoes', methods=['POST'])
def adicionar_transacao():
    dados = request.json

    data = datetime.now().strftime(FORMATO_DATA)

    with open(ARQUIVO, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([
            dados['usuario'],   # 👈 NOVO
            data,
            dados['valor'],
            dados['categoria'],
            dados['tipo'],
            dados['descricao']
        ])

    return jsonify({
        "data": data,
        "valor": dados['valor'],
        "categoria": dados['categoria'],
        "tipo": dados['tipo'],
        "descricao": dados['descricao']
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)