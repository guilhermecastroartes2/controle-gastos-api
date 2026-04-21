from utils import adicionar_transacao, listar_transacoes, filtrar_por_periodo
from relatorios import resumo_financeiro, grafico_categorias
from datetime import datetime

def menu():
    while True:
        print("""
              ===== CONTROLE DE GASTOS =====
              1 - Adicionar Receita
              2 - Adicionar Despesa
              3 - Listar Transações
              4 - Ver Resumo
              5 - Filtrar por Período
              6 - Ver Gráfico de Gastos
              7 - Sair
              """)
        
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            adicionar_transacao("receita")
        elif opcao == "2":
            adicionar_transacao("despesa")
        elif opcao == "3":
            listar_transacoes()
        elif opcao == "4":
            resumo_financeiro()
        elif opcao == "5":
            inicio = input("Data início (YYYY-MM-DD): ")
            fim = input("Data fim (YYYY-MM-DD): ")

            data_inicio = datetime.strptime(inicio, '%Y-%m-%d')
            data_fim = datetime.strptime(fim, '%Y-%m-%d')

            resultados = filtrar_por_periodo(data_inicio, data_fim)

            for r in resultados:
                print(r)
        
        elif opcao == "6":
            grafico_categorias()

        elif opcao == "7":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")


if __name__ == "__main__":
    menu()


