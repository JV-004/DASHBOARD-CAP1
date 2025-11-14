import streamlit as st
import oracledb
import pandas as pd
import json
from datetime import datetime
from config import constants
from services.weather_service import obtendo_dados_climaticos
from database.db_handler import conexao_db
from utils.file_handler import *
import os

st.title('Prevenção contra pragas 2.000')

cultura = st.selectbox(
    "**Selecione uma cultura:**",
    constants.LISTAS_CULTURAS
)
cultura = cultura.lower()

cidade = st.text_input(label='**Cidade**')


def pesquisando(cidade):
    temperatura, umidade = obtendo_dados_climaticos(cidade)
    st.write(temperatura, umidade)

    if temperatura is None or umidade is None:
        st.error(f'''Temperatura ou umidade vazios:\n
                    Temperatura: {temperatura}
                    umidade: {umidade}''')
    return temperatura, umidade


# Obter dados climáticos
# Usa a API OpenWeatherMap para obter os dados climáticos
# referentes à temperatura e a umidade


def calcular_risco(cultura, temperatura, umidade):
    risco = None
    if cultura in constants.FAIXAS_RISCO:
        for faixa in constants.FAIXAS_RISCO[cultura]:
            temp_min, umid_min, nivel_risco = faixa
            if temperatura >= temp_min and umidade >= umid_min:
                risco = nivel_risco
                break
    return risco


if st.button('Pesquisa'):
    temperatura, umidade = pesquisando(cidade)
    risco = calcular_risco(cultura, temperatura, umidade)
    recomendacao = constants.RECOMENDACOES.get(
        risco, 'Recomendação não disponível')

    try:
        with conexao_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO alertas_pragas 
                    (cultura, temperatura, umidade, risco, recomendacao, data_registro, cidade)
                    VALUES (:1, :2, :3, :4, :5, SYSDATE, :6)
                """, [cultura, temperatura, umidade, risco, recomendacao, cidade])
                conn.commit()
    except oracledb.Error as e:
        st.error('Erro')

    alertas = []
    alertas.append({
        'cultura': cultura.capitalize(),
        'cidade': cidade.title(),
        'data': datetime.now().isoformat(),
        'temperatura': round(temperatura, 2) if temperatura is not None else None,
        'umidade': umidade,
        'risco': risco,
        'recomendacao': recomendacao
    })


def buscar_todos_alertas() -> list[dict]:
    """
    Busca TODOS os registros da tabela ALERTAS_PRAGAS
    """
    sql = "SELECT * FROM alertas_pragas ORDER BY data_registro"

    alertas = []
    try:
        with conexao_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql)
                colunas = [desc[0].lower() for desc in cursor.description]
                for row in cursor.fetchall():
                    alertas.append(dict(zip(colunas, row)))
    except oracledb.Error as e:
        print(f"Erro no banco: {e}")

    return alertas


alertas = buscar_todos_alertas()
df_alertas = pd.DataFrame(alertas)
st.write("### Relátorio")
st.dataframe(df_alertas, use_container_width=True)

# Gerar recomendação
# Salvar no banco de dados


# Chamas as funções responsaveis por gerar relatorioas JSON e txt
# que irão armasenas as dados obtidos pelas analises e fornecidos pela
# API OpenWeatherMap


# --- Após criar df_alertas (como no exemplo anterior) ---

# 1. GERA TXT (formato legível)
txt_content = "=== RELATÓRIO DE ALERTAS ===\n\n"
for _, row in df_alertas.iterrows():
    txt_content += f"Cultura:       {row['cultura']}\n"
    txt_content += f"Cidade:        {row['cidade']}\n"
    txt_content += f"Data:          {row['data_registro']}\n"
    txt_content += f"Temperatura:   {row['temperatura']}°C\n"
    txt_content += f"Umidade:       {row['umidade']}%\n"
    txt_content += f"Risco:         {row['risco']}\n"
    txt_content += f"Recomendação:  {row['recomendacao']}\n"
    txt_content += "-" * 40 + "\n"

# 2. GERA CSV (usando pandas)
csv_content = df_alertas.to_csv(index=False, encoding='utf-8')

# 3. DOWNLOADS NO STREAMLIT
colunas = st.columns(2)

with colunas[0]:
    st.download_button(
        label="Baixar como TXT",
        data=txt_content,
        file_name="relatorio_alertas.txt",
        mime="text/plain"
    )

with colunas[1]:
    st.download_button(
        label="Baixar como CSV",
        data=csv_content,
        file_name="relatorio_alertas.csv",
        mime="text/csv"
    )
