# src/main.py
import oracledb
from datetime import datetime
from config import constants
from services.weather_service import obtendo_dados_climaticos
from database.db_handler import conexao_db
from utils.file_handler import *

def formatar_culturas():
    #Exibi uma lista formatada com 15 culturas disponíveis para o usuario escolher.
    for i, cultura in enumerate(constants.LISTAS_CULTURAS):
        print(f'\033[33;1m{i+1:02} - {cultura:12}\033[m ', end='')
        if (i + 1) % 3 == 0:
            print()  # Nova linha a cada 3 itens
        else:
            print(end='| ')

def main():
    """lista que armazena os registros gerados pelo programa
    com os dados sobre a cultura e a cidade onde ela
    será plantada disponibilizados pelo usuario"""
    alertas = []
    print('\033[34;1;4m-=-=-=-=- PREVENÇÃO DE PRAGAS 2.000 -=-=-=-=-\033[m\n')

    #Loop principal que exisbe o menu repedidamente até que o usuario encerre a aplicação
    while True:
        try:
            print(('\n\033[1;36m[1] Consultar cultura'
                   '\n[2] Exibir relatório completo'
                   '\n[3] Exibir relatório resumido'
                   '\n[4] Sair\033[m'))
            opcao = int(input('Escolha uma opção: '))

            match opcao:
                case 1:
                    # Exibir menu com a lista formatada cde 15 culturas
                    formatar_culturas()

                    #Dados de entrada: O nome da cultura que o usuario deseja analisar
                    cultura = input('\n\nDigite o nome da cultura: ').lower().strip()
                    if not cultura:
                        raise ValueError("Entrada vazia")

                    # Validar cultura
                    if cultura.capitalize() not in constants.LISTAS_CULTURAS:
                        print('\033[1;31mCultura inválida. Tente novamente.\033[m')
                        continue

                    """ Capturar cidade:
                    Dados de entrada: cidade que o usuario deseja analisar a possibilidade 
                    de pragas"""
                    cidade = input('Digite a cidade (Brasil): ').strip()
                    if not cidade.replace(' ', '').isalpha():
                        raise ValueError("Nome de cidade inválido")

                    """Obter dados climáticos
                    Usa a API OpenWeatherMap para obter os dados climáticos 
                    referentes à temperatura e a umidade"""
                    temperatura, umidade = obtendo_dados_climaticos(cidade)
                    if temperatura is None or umidade is None:
                        continue  # Volta para o início do loop

                    # Determinar risco
                    """Loop que analisa em qual faixa de risco (baixo, médio ou alto)
                    Aquela cultura está naquela cidade baseando-se na temperatura 
                    e na umidade"""
                    risco = None
                    for faixa in constants.FAIXAS_RISCO[cultura]:
                        temp_min, umid_min, nivel_risco = faixa
                        if temperatura >= temp_min and umidade >= umid_min:
                            risco = nivel_risco
                            break

                    # Gerar recomendação
                    recomendacao = constants.RECOMENDACOES.get(risco, 'Recomendação não disponível')

                    # Exibir relatório
                    print("\n\033[34;1;4m-=-=-=- Relatório Detalhado -=-=-=-\033[m")
                    print(f"{'Cultura:':<20} {cultura.capitalize()}")
                    print(f"{'Local:':<20} {cidade.upper()}")
                    print(f"{'Temperatura Atual:':<20} {temperatura:.1f}°C")
                    print(f"{'Umidade Relativa:':<20} {umidade}%")
                    print(f"{'Nível de Risco:':<20} {risco.upper() if risco else 'Desconhecido'}")
                    print(f"{'Ações Recomendadas:':<20} {recomendacao}")
                    print("-" * 40)

                    # Salvar no banco de dados
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
                        print(f'\033[1;31mErro DB: {e}\033[m')

                    alertas.append({
                        'cultura': cultura.capitalize(),
                        'cidade': cidade.title(),
                        'data': datetime.now().isoformat(),
                        'temperatura': round(temperatura, 2),
                        'umidade': umidade,
                        'risco': risco,
                        'recomendacao': recomendacao
                    })
                    """Chamas as funções responsaveis por gerar relatorioas JSON e txt
                    que irão armasenas as dados obtidos pelas analises e fornecidos pela 
                    API OpenWeatherMap"""
                    relatorio_json(alertas)
                    relatorio_completo_txt(alertas[-1])
                    relatorio_resumido_txt(alertas[-1])
                    alertas.clear()

                case 2:
                    #Exibe o relotório completo que foi gerado
                    exibir_relatorio()

                case 3:
                    """exibe uma versão resumida do relatorio com apenas os dados
                     da cultura, o risco e a recomendação da ação necessaria,  
                     com o objetivo de facilitar a visualização do usuario
                     (a cidade não é apresentada neste relatorio pois presumi-se
                     que os usuarios deste programa provavelmente iriam gerar 
                     relatorios apenas para a mesma cidade)"""
                    exibir_relatorio_resumido()

                case 4:
                    print('\n\033[1;32mRelatório final gerado em '
                          'data/relatorio_pragas.json\033[m')
                    break
                case _:
                    print('\033[1;31mOpção inválida. Escolha 1, 2, 3 ou 4.\033[m')

            # Opção para novo ciclo
            continuar = input('\nDeseja abrir o menu de opções? (s/n): ').lower()
            if continuar != 's':
                print('\n\033[1;32mRelatório final gerado em data/relatorio_pragas.json\033[m')
                break

        except KeyboardInterrupt:
            print('\n\n\033[1;33mOperação cancelada pelo usuário.\033[m')
            break
        except Exception as e:
            print(f'\n\033[1;31mErro inesperado: {e}\033[m')
            continue

if __name__ == '__main__':
    main()