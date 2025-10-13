import pandas as pd
import sqlite3
import openpyxl
from conect_banco_demo import saldo_por_data
import os

def gerar_relatorio(inicio, fim, caminho_arquivo):
    # Conecta ao banco
    conn = sqlite3.connect("./igreja.db")
    query = """
        SELECT 
            id_movimento,
            data,
            CASE 
                WHEN movimento = 1 THEN 'Entrada'
                WHEN movimento = 0 THEN 'Saída'
            END AS tipo_mov,
            tipo_movimento,
            valor,
            obs
        FROM movimento_financeiro
        WHERE date(REPLACE(data, '/', '-')) BETWEEN date(?) AND date(?)
        ORDER BY date(REPLACE(data, '/', '-')) ASC;
        """
    ""

    tabelas = pd.read_sql_query(query, conn, params=(inicio, fim))
    print("inicio:",inicio)
    print("fim:",fim)
    print("tabelas:",tabelas)
    tabelas['data'] = pd.to_datetime(tabelas['data'])

    # Soma valores por tipo de movimento
    movimento_valor = {}
    for tipo in tabelas['tipo_movimento'].unique():
        movimento_valor[tipo] = tabelas[tabelas['tipo_movimento'] == tipo]['valor'].sum()

    # Dicionários de receitas e despesas
    receitas = {
        'Dízimos:': 0,
        'Ofertas:': 0,
        'Ofertas Missionárias:': 0,
        'Ofertas Específicas:': 0,
        'Receitas Financeiras:': 0,
        'Empréstimos IPB / JPEF:': 0,
        'Parcerias:': 0,
        'Outras Receitas:': 0
    }

    despesas = {
        "Patrimônio:": 0,
        "Causas Locais:": 0,
        "Evangelismo Local:": 0,
        "Missões:": 0,
        "Ação Social:": 0,
        "Sustento Pastoral:": 0,
        "Verba Presbiterial:": 0,
        "Dízimo ao Supremo Concílio:": 0,
        "Empréstimos IPB / JPEF:": 0,
        "Outras Despesas:": 0
    }

    # Preenche valores usando .get() para evitar KeyError
    for chave in receitas.keys():
        receitas[chave] = movimento_valor.get(chave, 0)

    for chave in despesas.keys():
        despesas[chave] = movimento_valor.get(chave, 0)

    # Carrega planilha modelo
    wb = openpyxl.load_workbook("./relatorio_igreja.xlsx")
    sheet = wb.active

    # Preenche receitas
    sheet["H8"] = saldo_por_data(data=inicio)
    sheet["H10"] = receitas["Dízimos:"]
    sheet["H11"] = receitas["Ofertas:"]
    sheet["H12"] = receitas["Ofertas Missionárias:"]
    sheet["H13"] = receitas["Ofertas Específicas:"]
    sheet["H14"] = receitas["Receitas Financeiras:"]
    sheet["H15"] = receitas["Empréstimos IPB / JPEF:"]
    sheet["H16"] = receitas["Parcerias:"]
    sheet["H17"] = receitas["Outras Receitas:"]

    # Preenche despesas
    sheet["H22"] = despesas["Patrimônio:"]
    sheet["H23"] = despesas["Causas Locais:"]
    sheet["H24"] = despesas["Evangelismo Local:"]
    sheet["H25"] = despesas["Missões:"]
    sheet["H26"] = despesas["Ação Social:"]
    sheet["H27"] = despesas['Sustento Pastoral:']
    sheet["H28"] = despesas["Verba Presbiterial:"]
    sheet["H29"] = despesas['Dízimo ao Supremo Concílio:']
    sheet["H30"] = despesas['Empréstimos IPB / JPEF:']
    sheet["H31"] = despesas['Outras Despesas:']

    # Salva planilha no caminho fornecido
    wb.save(caminho_arquivo)
    
    return f"Arquivo gerado em {os.path.abspath(caminho_arquivo)}"
if __name__ == "__main__":
    # Exemplo de datas e caminho para teste
    inicio_teste = "2023-01-01"
    fim_teste = "2025-12-31"
    caminho_saida = "./relatorio_teste.xlsx"

    try:
        resultado = gerar_relatorio(inicio_teste, fim_teste, caminho_saida)
        print(" Teste concluído com sucesso!")
        print(resultado)
    except Exception as e:
        print(" Erro ao gerar relatório:")
        print(e)
