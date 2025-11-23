import requests
import json

# Esta URL dispara o Lambda SNS (relatorios-farm-tech)
API_ENDPOINT = "https://19rfo7d5q0.execute-api.us-east-2.amazonaws.com/prod/relatorios" 

def enviar_alerta_bomba_ligada(umidade, pH, fosforo, potassio):
    """
    Envia um alerta de "Bomba Ligada" para o API Gateway/SNS.
    """
    
    # Monta a lista de minerais presentes para a mensagem
    minerais_presentes = []
    if fosforo == 1:
        minerais_presentes.append("Fósforo")
    if potassio == 1:
        minerais_presentes.append("Potássio")
    
    minerais_str = " e ".join(minerais_presentes) if minerais_presentes else "Nenhum"
    
    # Formata o corpo da mensagem conforme o modelo solicitado
    # No seu arquivo envio_email.py

    acao_corretiva_msg = f"""Ligue a bomba de água

    --- Dados Inseridos ---
    Porcentagem da umidade: {umidade}%
    Valor pH: {pH}
    Minerais: {minerais_str}
    -----------------------"""

    dados_do_alerta = {
        # O Lambda SNS espera 'sensor' e 'acao_corretiva'
        "sensor": "Status da Bomba de Água",
        "leitura": f"UMIDADE {umidade}% / pH {pH}",
        "acao_corretiva": acao_corretiva_msg,
        "id_alerta": "ALERTA_BOMBA_LIGADA"
    }
    
    try:
        response = requests.post(
            API_ENDPOINT, 
            data=json.dumps(dados_do_alerta),
            headers={'Content-Type': 'application/json'}
        )
        
        # Não usamos st.success aqui, pois esta função é chamada por fora do Streamlit loop
        if response.status_code == 200:
            print("✅ Alerta de Bomba Ligada enviado para o SNS.")
            return True
        else:
            print(f"❌ Erro ao enviar alerta SNS. Código HTTP: {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão com a AWS API Gateway: {e}")
        return False