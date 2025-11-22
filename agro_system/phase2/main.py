# ============================================
# FASE 2 - Banco de Dados (Versão Mock Segura)
# ============================================

# Este módulo simula a Fase 2 para que o dashboard funcione
# mesmo sem o banco Oracle ou sem a entrega oficial do grupo.

import pandas as pd

# ---------------------------
# Simula tabelas do BD
# ---------------------------
def carregar_tabelas():
    """
    Retorna tabelas simuladas para o Streamlit exibir.
    Não requer banco de dados e nunca gera erro.
    """

    dados = {
        "ID": [1, 2, 3],
        "Sensor": ["S-01", "S-02", "S-03"],
        "Umidade (%)": [45, 55, 63],
        "Temperatura (°C)": [23.4, 24.1, 22.8]
    }

    df = pd.DataFrame(dados)
    return df


# ---------------------------
# Simula consultas SQL
# ---------------------------
def executar_consultas():
    """
    Simula execução de consultas SQL, retornando
    um dicionário simples que o Streamlit pode exibir.
    """

    resultado = {
        "consulta": "SELECT * FROM sensores LIMIT 3;",
        "mensagem": "Consulta executada com sucesso (modo simulado).",
        "linhas_encontradas": 3,
        "dados": [
            {"sensor": "S-01", "umidade": 45, "temperatura": 23.4},
            {"sensor": "S-02", "umidade": 55, "temperatura": 24.1},
            {"sensor": "S-03", "umidade": 63, "temperatura": 22.8},
        ]
    }

    return resultado
# Código da phase2

