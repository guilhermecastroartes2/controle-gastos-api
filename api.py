from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

DB_NAME = "controle_gastos.db"

def conectar():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Isso permite acessar colunas pelo nome (ex: linha['valor'])
    return conn

# Função para criar as tabelas se não existirem
def init_db():
    with conectar() as conn:
        cursor = conn.cursor()
        # Tabela de Usuários
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                email TEXT PRIMARY KEY,
                senha TEXT NOT NULL
            )
        """)
        # Tabela de Transações
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT,
                data TEXT,
                valor REAL,
                categoria TEXT,
                tipo TEXT,
                descricao TEXT,
                FOREIGN KEY (email) REFERENCES usuarios (email)
            )
        """)
        conn.commit()

init_db()

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    try:
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO usuarios (email, senha) VALUES (?, ?)", (data["email"], data["senha"]))
            conn.commit()
        return jsonify({"msg": "ok"})
    except sqlite3.IntegrityError:
        return jsonify({"erro": "Este email já está cadastrado"}), 400

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (data["email"], data["senha"]))
        user = cursor.fetchone()
    
    if user:
        return jsonify({"msg": "ok"})
    return jsonify({"erro": "Login ou senha incorretos"}), 401

@app.route("/transacoes", methods=["GET"])
def listar():
    email = request.args.get("email")
    with conectar() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transacoes WHERE email = ? ORDER BY data DESC", (email,))
        linhas = cursor.fetchall()
    
    # Converte os resultados para uma lista de dicionários
    dados = [dict(linha) for linha in linhas]
    return jsonify(dados)

@app.route("/transacoes", methods=["POST"])
def adicionar():
    data = request.json
    data_atual = datetime.now().strftime("%d/%m/%Y %H:%M") # Formato brasileiro
    
    try:
        valor_float = float(data["valor"])
        with conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO transacoes (email, data, valor, categoria, tipo, descricao)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (data["email"], data_atual, valor_float, data["categoria"], data["tipo"], data["descricao"]))
            conn.commit()
            
        return jsonify({
            "email": data["email"],
            "data": data_atual,
            "valor": valor_float,
            "categoria": data["categoria"],
            "tipo": data["tipo"],
            "descricao": data["descricao"]
        })
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

if __name__ == '__main__':
    # Usando host 0.0.0.0 para que o celular consiga acessar o PC na mesma rede
    
    @app.route("/transacoes/<int:id>", methods=["DELETE"])
    def deletar(id):
        try:
            with conectar() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM transacoes WHERE id = ?", (id,))
                conn.commit()
            return jsonify({"msg": "Removido com sucesso"})
        except Exception as e:
            return jsonify({"erro": str(e)}), 400    
    app.run(host="0.0.0.0", port=5000, debug=True)