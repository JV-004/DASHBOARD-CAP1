import sqlite3
import time

# Cores no terminal
yellow = '\033[1;33m'
red = '\033[1;31m'
close = '\033[m'


# Função para simular dados do Wokwi (entrada manual, um a um)
def simulate_wokwi_data():
    print("Digite os valores do Monitor Serial do Wokwi:")

    while True:
        try:
            umidade = float(input("umidade: "))
            if 0 <= umidade <= 100:
                break
            else:
                print('Digite um valor entre 0 e 100 para a umidade')
        except ValueError:
            print('Digite um Valor numérico')

    while True:
        try:
            pH = float(input('pH: [0 a 14]: '))
            if 0 <= pH <= 14:
                break
            else:
                print('Digite um valor entre 0 e 14 para o pH')
        except ValueError:
            print('Digite um Valor numérico')

    while True:
        status = input(f'Há presença de {red}FOSFORO{close}? [S/N]: ')[0].upper()
        if status in 'S':
            fosforo = 1
            break
        elif status in 'N':
            fosforo = 0
            break
        else:
            print('Opção inválida, por favor digite S ou N')

    while True:
        status = input(f'Há presença de {red}POTASSIO{close}? [S/N]: ')[0].upper()
        if status in 'S':
            potassio = 1
            break
        elif status in 'N':
            potassio = 0
            break
        else:
            print('Opção inválida, por favor digite S ou N')

    if umidade < 30 and 5 <= pH <= 7 and fosforo == 1 and potassio == 1:
        bomba_ativa = 1
        print('Bomba ligada')
    else:
        bomba_ativa = 0
        print('Bomba Desligada')
    return umidade, pH, fosforo, potassio, bomba_ativa


# Função para conectar ao banco de dados e criar tabelas se não existirem
def connect_db():
    conn = sqlite3.connect('irrigation.db')
    cursor = conn.cursor()
    #Criar tabela T_Medicoes se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS T_Medicoes(
            id_medicao INTEGER PRIMARY KEY AUTOINCREMENT,
            data_hora DATETIME,
            umidade REAL,
            pH REAL,
            fosforo INTEGER,
            potassio INTEGER,
            bomba_ativa INTEGER
        )
    ''')
    
    #Criar tablea T_Configuracoes se não existir
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS T_Configuracoes(
            id_config INTEGER PRIMARY KEY AUTOINCREMENT,
            limite_umidade REAL,
            pH_min REAL,
            pH_max REAL
        )
    ''')
    return conn, conn.cursor()


# Função para consultar (Read) todas as medições
def read_medicoes(cursor):
    cursor.execute("SELECT * FROM T_Medicoes")
    medicoes = cursor.fetchall()
    if not medicoes:
        print("Nenhum dado encontrado na tabela T_Medicoes.")
    else:
        print(f"\n{yellow}Lista de Medições:{close}")
        for medicao in medicoes:
            print(f"ID: {medicao[0]:2} | Data/Hora: {medicao[1]} | Umidade: {medicao[2]:6} | pH: {medicao[3]:5} | "
                  f"Fósforo: {medicao[4]} | Potássio: {medicao[5]} | Bomba Ativa: {medicao[6]}")


# Função para atualizar (Update) uma medição
def update_medicao(cursor, conn):
    read_medicoes(cursor)
    try:
        id_medicao = int(input("Digite o ID da medição que deseja atualizar: "))
        cursor.execute("SELECT * FROM T_Medicoes WHERE id_medicao = ?", (id_medicao,))
        if cursor.fetchone() is None:
            print(f"Medição com ID {id_medicao} não encontrada!")
            return

        print("\nDigite os novos valores (deixe em branco para manter o valor atual):")
        umidade = input("Nova umidade (ou Enter para manter): ")
        pH = input("Novo pH (ou Enter para manter): ")
        fosforo_input = input(f"Novo status de {red}FOSFORO{close} [S/N] (ou Enter para manter): ")
        potassio_input = input(f"Novo status de {red}POTASSIO{close} [S/N] (ou Enter para manter): ")

        query = "UPDATE T_Medicoes SET "
        params = []
        if umidade:
            query += "umidade = ?, "
            params.append(float(umidade))
        if pH:
            query += "pH = ?, "
            params.append(float(pH))
        if fosforo_input:
            fosforo = 1 if fosforo_input.upper() == 'S' else 0
            query += "fosforo = ?, "
            params.append(fosforo)
        if potassio_input:
            potassio = 1 if potassio_input.upper() == 'S' else 0
            query += "potassio = ?, "
            params.append(potassio)

        if params:
            query = query.rstrip(", ") + " WHERE id_medicao = ?"
            params.append(id_medicao)
            cursor.execute(query, params)
            conn.commit()

            # Recalcular bomba_ativa com base nos novos valores
            cursor.execute("SELECT umidade, pH, fosforo, potassio, bomba_ativa FROM T_Medicoes WHERE id_medicao = ?", (id_medicao,))
            current = cursor.fetchone()
            new_umidade = float(umidade) if umidade else current[0]
            new_pH = float(pH) if pH else current[1]
            new_fosforo = 1 if fosforo_input and fosforo_input.upper() == 'S' else (
                0 if fosforo_input and fosforo_input.upper() == 'N' else current[2])
            new_potassio = 1 if potassio_input and potassio_input.upper() == 'S' else (
                0 if potassio_input and potassio_input.upper() == 'N' else current[3])

            if new_umidade < 30 and 5 <= new_pH <= 7 and new_fosforo == 1 and new_potassio == 1:
                bomba_ativa = 1
                print('Bomba ligada')
            else:
                bomba_ativa = 0
                print('Bomba Desligada')

            # Atualizar bomba_ativa no banco
            cursor.execute("UPDATE T_Medicoes SET bomba_ativa = ? WHERE id_medicao = ?", (bomba_ativa, id_medicao))
            conn.commit()
            print("Medição atualizada com sucesso!")
        else:
            print("Nenhum valor foi alterado.")
    except ValueError as e:
        print(f"Erro: Digite valores válidos! ({e})")


# Função para deletar (Delete) uma medição
def delete_medicao(cursor, conn):
    read_medicoes(cursor)
    try:
        id_medicao = int(input("Digite o ID da medição que deseja deletar: "))
        cursor.execute("SELECT * FROM T_Medicoes WHERE id_medicao = ?", (id_medicao,))
        if cursor.fetchone() is None:
            print(f"Medição com ID {id_medicao} não encontrada!")
            return
        cursor.execute("DELETE FROM T_Medicoes WHERE id_medicao = ?", (id_medicao,))
        conn.commit()
        print("Medição deletada com sucesso!")
    except ValueError:
        print("Erro: Digite um ID válido!")


# Função principal com menu CRUD
def main():
    conn, cursor = connect_db()

    try:
        while True:
            print(f"\n{yellow}=== Menu CRUD ==={close}")
            print("1. Inserir nova medição (Create)")
            print("2. Consultar medições (Read)")
            print("3. Atualizar medição (Update)")
            print("4. Deletar medição (Delete)")
            print("5. Sair")
            opcao = input("Escolha uma opção [1-5]: ")

            if opcao == '1':
                umidade, pH, fosforo, potassio, bomba_ativa = simulate_wokwi_data()
                cursor.execute("""
                    INSERT INTO T_Medicoes (data_hora, umidade, pH, fosforo, potassio, bomba_ativa)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (time.strftime('%Y-%m-%d %H:%M:%S'), umidade, pH, fosforo, potassio, bomba_ativa))
                conn.commit()
                print("Dados salvos no banco!")
            elif opcao == '2':
                read_medicoes(cursor)
            elif opcao == '3':
                update_medicao(cursor, conn)
            elif opcao == '4':
                delete_medicao(cursor, conn)
            elif opcao == '5':
                print("Saindo do programa...")
                break
            else:
                print("Opção inválida! Escolha entre 1 e 5.")

    except KeyboardInterrupt:
        print("\nPrograma encerrado.")
    except Exception as e:
        print(f"Erro: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    main()