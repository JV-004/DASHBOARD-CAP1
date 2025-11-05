import requests
from config.settings import API_KEY

def obtendo_dados_climaticos(cidade):
    """
    Essa função faz uma requisição para a API OpenWeatherMap, e captura dados climaticos de uma
    cidade específica digitada pelo usuario

    Dados de entrada: cidade
    Dados de saída: retorta a temperatura e a umidade daquela cidade naquele momento
    """
    base_url = 'http://api.openweathermap.org/data/2.5/weather?'
    url_completa = f'{base_url}appid={API_KEY}&q={cidade}'
    
    try:
        """
        Envia a requisição atraves da API requests, 
        salva os dados coletados em formato de arquivo JSON dentro de 'data'
        """
        response = requests.get(url_completa)
        data = response.json()

        #Retorna os dados de temperatura e umidade
        if data['cod'] == 200:
            return data['main']['temp'] - 273.15, data['main']['humidity']
        print(f"ERRO: Cidade '{cidade}' não encontrada")
        return None, None
    except Exception as e:
        print(f'ERRO na API: {e}')
        return None, None