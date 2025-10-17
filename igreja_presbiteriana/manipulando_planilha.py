import pandas as pd
import sqlite3
import openpyxl
from conect_banco import saldo_por_data
import os

def gerar_relatorio(inicio, fim, caminho_arquivo):
    """
    Gera um relatório financeiro da igreja entre duas datas
    e preenche um modelo de planilha Excel.
    """
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

    tabelas = pd.read_sql_query(query, conn, params=(inicio, fim))
    print(f"Período do relatório: {inicio} até {fim}")
    print("Registros encontrados:", len(tabelas))

    # Caso não haja registros
    if tabelas.empty:
        print(" Nenhum dado encontrado no período informado.")
        return None

    # Converte a coluna 'data' para datetime
    tabelas['data'] = pd.to_datetime(tabelas['data'], errors='coerce')

    # Soma valores por tipo de movimento (Ex: "Dízimos", "Ofertas")
    movimento_valor = tabelas.groupby('tipo_movimento')['valor'].sum().to_dict()
    print("Movimento valor:",movimento_valor)
    # Define categorias de receitas e despesas
    receitas = {
        'Dízimos': 0,
        'Ofertas': 0,
        'Ofertas Missionárias': 0,
        'Ofertas Específicas': 0,
        'Receitas Financeiras': 0,
        'Empréstimos IPB / JPEF': 0,
        'Parcerias': 0,
        'Outras Receitas': 0
    }

    despesas = {
        "Patrimônio": 0,
        "Causas Locais": 0,
        "Evangelismo Local": 0,
        "Missões": 0,
        "Ação Social": 0,
        "Sustento Pastoral": 0,
        "Verba Presbiterial": 0,
        "Dízimo ao Supremo Concílio": 0,
        "Empréstimos IPB / JPEF": 0,
        "Outras Despesas:": 0
    }

    # Preenche valores nas categorias (sem ":" no nome)
    for chave in receitas:
         if  chave in movimento_valor.keys():
                receitas[chave] = movimento_valor[chave]
   

    for chave in despesas:
           if  chave in movimento_valor.keys():
               despesas[chave] = movimento_valor[chave]
    print("Despessas:",despesas)
    print("Receitas:",receitas)
    # Carrega planilha modelo
    wb = openpyxl.load_workbook("./relatorio_igreja.xlsx")
    sheet = wb.active

    # Preenche receitas
    try:
        saldo_inicial = saldo_por_data(data=inicio)
    except Exception:
        saldo_inicial = 0

    sheet["H8"] = saldo_inicial
    sheet["H10"] = receitas["Dízimos"]
    sheet["H11"] = receitas["Ofertas"]
    sheet["H12"] = receitas["Ofertas Missionárias"]
    sheet["H13"] = receitas["Ofertas Específicas"]
    sheet["H14"] = receitas["Receitas Financeiras"]
    sheet["H15"] = receitas["Empréstimos IPB / JPEF"]
    sheet["H16"] = receitas["Parcerias"]
    sheet["H17"] = receitas["Outras Receitas"]

    # Preenche despesas
    sheet["H22"] = despesas["Patrimônio"]
    sheet["H23"] = despesas["Causas Locais"]
    sheet["H24"] = despesas["Evangelismo Local"]
    sheet["H25"] = despesas["Missões"]
    sheet["H26"] = despesas["Ação Social"]
    sheet["H27"] = despesas["Sustento Pastoral"]
    sheet["H28"] = despesas["Verba Presbiterial"]
    sheet["H29"] = despesas["Dízimo ao Supremo Concílio"]
    sheet["H30"] = despesas["Empréstimos IPB / JPEF"]
    sheet["H31"] = despesas["Outras Despesas:"]

    wb.save(caminho_arquivo)
    conn.close()
    print(despesas)
    caminho_abs = os.path.abspath(caminho_arquivo)
    print(f" Relatório gerado com sucesso: {caminho_abs}")
    return caminho_abs



