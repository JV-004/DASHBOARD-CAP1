import json
from datetime import datetime
import os

base_dir = os.path.dirname(__file__)
caminho = os.path.join(base_dir, 'data', 'relatorio_completo.txt')
caminho_resumido = os.path.join(base_dir, 'data', 'relatorio_resumido.txt')
caminho_json = os.path.join(base_dir, 'data', 'relatorio_pragas.json')

def relatorio_completo_txt(alerta):
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    """
    Gera um arquivo txt com o relatório completo com
    todos os dados relevantes coletados para a prevenção contra pragas e as recomendações

    Dados de entrada: lista alertas que contem todos os dados relevantes
    """

    with open(caminho, 'a', encoding='utf-8') as arquivo:
#       conteudo = arquivo.read()

#    with open('Python_e_alem/src/data/relatorio_completo.txt', 'a', encoding='utf-8') as arquivo:
        arquivo.write('\n-=-=-=- Alerta Salvo -=-=-=-\n')
        arquivo.write(f"{'Cultura:':<20} {alerta['cultura']}\n")
        arquivo.write(f"{'Cidade:':<20} {alerta['cidade']}\n")
        arquivo.write(f"{'Data:':<20} {alerta['data']}\n")
        arquivo.write(f"{'Temperatura:':<20} {alerta['temperatura']}°C\n")
        arquivo.write(f"{'Umidade:':<20} {alerta['umidade']}%\n")
        risco = alerta['risco'].upper() if alerta['risco'] else 'Desconhecido'
        arquivo.write(f"{'Nível de Risco:':<20} {risco}\n")
        arquivo.write(f"{'Recomendação:':<20} {alerta['recomendacao']}\n")
        arquivo.write('-' * 40 + '\n')

def relatorio_resumido_txt(alerta):
    """
    Gera um arquivo txt com o relatório resumido contendo apenas os dados da
     cultura, risco (baixo, médio ou alto) e a recomendação do que se deve fazer

    Dados de entrada: lista alertas que contem todos os dados relevantes
    """
    with open('Python_e_alem/src/data/relatorio_resumido.txt', 'a', encoding='utf-8') as arquivo:
        risco = alerta['risco'].upper() if alerta['risco'] else 'Desconhecido'
        linha = f"{alerta['cultura']:<15} | {risco:<10} | {alerta['recomendacao']}\n"
        arquivo.write(linha)

def relatorio_resumido_txt(alerta):
    """
    Adiciona linha ao relatório resumido (cultura | risco | recomendação)
    """
    # Garante que a pasta 'data' existe
    os.makedirs(os.path.dirname(caminho_resumido), exist_ok=True)

    with open(caminho_resumido, 'a', encoding='utf-8') as arquivo:
        risco = alerta['risco'].upper() if alerta['risco'] else 'Desconhecido'
        linha = f"{alerta['cultura']:<15} | {risco:<10} | {alerta['recomendacao']}\n"
        arquivo.write(linha)

def relatorio_json(alertas):
    """
    Gera um arquivo JSON com o relatório completo com todos os dados relevantes

    Dados de entrada: lista alertas que contem todos os dados relevantes
    """
    try:
        os.makedirs(os.path.dirname(caminho_json), exist_ok=True)
        # Tenta ler o conteúdo existente
        try:
            with open(caminho_json, 'r', encoding='utf-8') as arquivo:
                dados_existentes = json.load(arquivo)
        except (FileNotFoundError, json.JSONDecodeError):
            dados_existentes = []

        # Adiciona novos alertas aos dados existentes
        dados_existentes.extend(alertas)

        # Salva o conteúdo atualizado
        with open(caminho_json, 'w', encoding='utf-8') as arquivo:
            json.dump(dados_existentes, arquivo, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"\033[1;31mErro ao salvar relatório JSON: {e}\033[m")
        
def exibir_relatorio():
    """
    Exibe o relatorio completo

    retorna: Todos os dados relevantes sobre cada analise de cada cultura que foram salvos
    """
    try:
        with open('Python_e_alem/src/data/relatorio_pragas.json', 'r', encoding='utf-8') as arquivo:
            alertas = json.load(arquivo)
            if not alertas:
                print("\033[1;33mNenhum alerta encontrado no relatório.\033[m")
                return

            print("\033[34;1;4m-=-=-=- Relatório de Pragas -=-=-=-\033[m")
            for alerta in alertas:
                print(f"{'Cultura:':<20} {alerta['cultura']}")
                print(f"{'Cidade:':<20} {alerta['cidade']}")
                print(f"{'Data:':<20} {alerta['data']}")
                print(f"{'Temperatura:':<20} {alerta['temperatura']}°C")
                print(f"{'Umidade:':<20} {alerta['umidade']}%")
                risco = alerta['risco'].upper() if alerta['risco'] else 'Desconhecido'
                print(f"{'Nível de Risco:':<20} {risco}")
                print(f"{'Recomendação:':<20} {alerta['recomendacao']}")
                print("-" * 40)
    except FileNotFoundError:
        print("\033[1;31mArquivo de relatório não encontrado.\033[m")
    except json.JSONDecodeError:
        print("\033[1;31mErro ao ler o arquivo JSON.\033[m")
    except Exception as e:
        print(f"\033[1;31mErro inesperado: {e}\033[m")

def exibir_relatorio_resumido():
    """
    Exibe um relatório resumido com dados sobre cultura, risco (baixo, médio, alto) e recomendações

    Retorna: A lista alertas com os dados formatados
    """
    try:
        with open('Python_e_alem/src/data/relatorio_pragas.json', 'r', encoding='utf-8') as arquivo:
            alertas = json.load(arquivo)
            if not alertas:
                print("\033[1;33mNenhum alerta encontrado no relatório.\033[m")
                return

            print("\033[34;1;4m-=-=-=- Relatório Resumido de Pragas -=-=-=-\033[m")
            print(f"{'Cultura':<15} | {'Risco':<10} | {'Recomendação':<30}")
            print("-" * 60)
            for alerta in alertas:
                risco = alerta['risco'].upper() if alerta['risco'] else 'Desconhecido'
                print(f"{alerta['cultura']:<15} | {risco:<10} | {alerta['recomendacao']:<30}")
            print("-" * 60)
    except FileNotFoundError:
        print("\033[1;31mArquivo de relatório não encontrado.\033[m")
    except json.JSONDecodeError:
        print("\033[1;31mErro ao ler o arquivo JSON.\033[m")
    except Exception as e:
        print(f"\033[1;31mErro inesperado: {e}\033[m")