from flask import Flask, request, jsonify
from flask_cors import CORS

import csv
from datetime import datetime


app = Flask(__name__)
CORS(app)

ARQUIVO = 'dados.csv'
FORMATO_DATA = '%Y-%m-%d'

@app.route('/')
def home():
    return "API de Controle de Gastos Rodando"

@app.route('/transacoes', methods=['GET'])
def listar_transacoes():
    dados = []

    try:
        with open(ARQUIVO, 'r') as file:
            reader = csv.reader(file)
            for linha in reader:
                if len(linha) < 4:
                    continue

                dados.append({
                    "data": linha[0],
                    "valor": linha[1],
                    "categoria": linha[2],
                    "tipo": linha[3],
                    "descricao": linha[4]
                })

    except FileNotFoundError:
        return jsonify([])
    
    return jsonify(dados)

@app.route('/transacoes', methods=['POST'])
def adicionar_transacao():
    dados = request.json

    nova = [
        datetime.now().strftime(FORMATO_DATA),
        dados['valor'],
        dados['categoria'],
        dados['tipo'],
        dados['descricao']
    ]

    with open(ARQUIVO, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(nova)

    return jsonify({"mensagem": "Transação adicionada"})

if __name__ == '__main__':
    app.run(debug=True)

