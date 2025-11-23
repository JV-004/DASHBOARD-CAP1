import requests
import json
import pandas as pd

# 🚨 SUA URL FINAL DO API GATEWAY CONECTADA AO ESTÁGIO 'prod'
API_ENDPOINT = "https://19rfo7d5q0.execute-api.us-east-2.amazonaws.com/prod/relatorios" 

def enviar_relatorio_por_email(df_registros: pd.DataFrame):
    """
    Converte o DataFrame de registros em texto plano e o envia
    como um relatório por e-mail via API Gateway/SNS.
    """
    
    # 1. Converter o DataFrame em uma string de texto formatada
    
    # Usamos o método to_string() para obter uma representação limpa do DataFrame em texto.
    # O parâmetro index=False garante que a coluna de índices do DataFrame não seja incluída.
    tabela_texto = df_registros.to_string(index=False)
    
    # 2. Montar o corpo da mensagem em Texto Plano
    
    corpo_alerta_texto = f"""
*** RELATÓRIO COMPLETO DE REGISTROS DA ESTUFA ***

Prezado(a) usuário(a),

Segue abaixo o relatório completo dos dados de monitoramento do solo e status da bomba.
Total de Registros: {len(df_registros)}

---------------------------------------------------------------------------------------------------------------------
{tabela_texto}
---------------------------------------------------------------------------------------------------------------------

Este relatório foi gerado automaticamente pelo sistema Farm-Tech.
"""

    # 3. Montar o payload para o API Gateway
    
    dados_do_alerta = {
        # Usamos 'acao_corretiva' para enviar o corpo do e-mail.
        "sensor": "Relatório de Registros Solicitado",
        "leitura": f"Total de {len(df_registros)} registros.",
        "acao_corretiva": corpo_alerta_texto, # Envia o texto simples
        "id_alerta": "RELATORIO_COMPLETO_TEXTO"
    }
    
    try:
        response = requests.post(
            API_ENDPOINT, 
            data=json.dumps(dados_do_alerta),
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            return True
        else:
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão com a AWS API Gateway: {e}")
        return False