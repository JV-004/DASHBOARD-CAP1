"""
Módulo de Sensores da Fase 4 (Simulação)
----------------------------------------
Este módulo simula os sensores utilizados no firmware do ESP32 criado
na fase anterior (Fase 4), mantendo a mesma lógica do hardware real,
mas funcionando 100% dentro do Python — ideal para integração com o
dashboard da Fase 7.

Sensores simulados:
- Umidade (DHT22)
- pH (via mapeamento do LDR)
- Presença de Fósforo (botão P)
- Presença de Potássio (botão K)

Atuador simulado:
- Bomba de irrigação (relé)

A lógica de acionamento da bomba segue o firmware real:
A bomba liga apenas se:
- umidade < 30
- pH entre 5 e 7
- fósforo == True
- potássio == True
"""

import random

def ler_sensores_simulado():
    """
    Simula a leitura dos sensores utilizados no ESP32 real.

    Retorna:
        dict: contendo:
            - umidade (float)
            - pH (float)
            - LDR (int)
            - fosforo (bool)
            - potassio (bool)
            - bomba (bool)
    """

    # --- Simulação da umidade (%), baseado no DHT22 real ---
    umidade = round(random.uniform(20, 80), 1)

    # --- Simulação do pH baseado na lógica do LDR ---
    # O LDR real retorna valores 0–4095, convertidos para pH 0–14
    ldr = random.randint(0, 4095)
    ph = round((ldr / 4095) * 14, 2)

    # --- Simulação dos botões P e K (Fósforo e Potássio) ---
    fosforo = random.choice([True, False])
    potassio = random.choice([True, False])

    # --- Lógica real da bomba (igual ao firmware C++) ---
    bomba = (umidade < 30) and (5 <= ph <= 7) and fosforo and potassio

    return {
        "umidade": umidade,
        "pH": ph,
        "LDR": ldr,
        "fosforo": fosforo,
        "potassio": potassio,
        "bomba": bomba
    }


# Função opcional (DEBUG) para ver os dados no terminal
if __name__ == "__main__":
    for _ in range(5):
        dados = ler_sensores_simulado()
        print(dados)
