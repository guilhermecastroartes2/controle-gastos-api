import csv
from datetime import datetime

ARQUIVO = "dados.csv"
FORMATO_DATA = '%Y-%m-%d'

def adicionar_transacao(tipo):
    valor = float(input("Valor: "))
    categoria = input("categoria: ")
    descricao = input("Descrição: ")
    data = datetime.now().strftime(FORMATO_DATA)

    with open(ARQUIVO, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([data, valor, categoria, tipo, descricao])

    print("Transação adicionada com sucesso!")

def listar_transacoes():
    try:
        with open(ARQUIVO, 'r') as file:
            reader = csv.reader(file)
            for linha in reader:
                print(linha)
    except FileNotFoundError:
        print("Nenhuma transação encontrada.")

def filtrar_por_periodo(data_inicio, data_fim):
    resultados = []

    try:
        with open(ARQUIVO, 'r') as file:
            reader = csv.reader(file)

            for linha in reader:
                if len(linha) < 4:
                    continue
                try:
                    data = datetime.strptime(linha[0], FORMATO_DATA)
                except ValueError:
                    continue # ignora linhas inválidas

                if data_inicio <= data <= data_fim:
                    resultados.append(linha)

    except FileNotFoundError:
        print("Nenhum dado encontrado.")

    return resultados
