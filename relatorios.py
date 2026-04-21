import csv
import matplotlib.pyplot as plt

ARQUIVO = 'dados.csv'


def resumo_financeiro():
    receitas = 0
    despesas = 0
    categorias = {}

    try:
        with open(ARQUIVO, 'r') as file:
            reader = csv.reader(file)

            for linha in reader:
                # validação de segurança
                if len(linha) < 4:
                    continue

                try:
                    valor = float(linha[1])
                except ValueError:
                    continue
                
                categoria = linha[2]
                tipo = linha[3]

                if tipo == 'receita':
                    receitas += valor
                else:
                    despesas += valor

                if categoria not in categorias:
                    categorias[categoria] = 0

                categorias[categoria] += valor

        saldo = receitas - despesas

        print(f"Receitas: R$ {receitas:.2f}")
        print(f"Despesas: R${despesas:.2f}")
        print(f"Saldo: R$ {saldo:.2f}")

    except FileNotFoundError:
                print("Nenhum dado encontrado.")

def grafico_categorias():
    categorias = {}

    try:
        with open(ARQUIVO, 'r') as file:
            reader = csv.reader(file)

            for linha in reader:
                if len(linha) < 4:
                    continue

                try:
                    valor = float(linha[1])
                except ValueError:
                    continue

                categoria = linha[2]
                tipo = linha[3]

                if tipo == 'despesa':
                    if categoria not in categorias:
                        categorias[categoria] = 0

                    categorias[categoria] += valor

        nomes = list(categorias.keys())
        valores = list(categorias.values())

        plt.figure()
        plt.bar(nomes, valores)
        plt.title('Gastos por Categoria')
        plt.xlabel('Categorias')
        plt.ylabel('Valor (R$)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    except FileNotFoundError:
        print("Nenhum dado encontrado.")
