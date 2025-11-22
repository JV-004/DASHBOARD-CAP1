from db_connection import conectar

# =============================
# CONSULTA 1 – T_REGISTROS
# =============================
def get_registros_sensores(limit=20):
    conn = conectar()
    if conn is None:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT ID_REGISTRO, DATA_HORA, UMIDADE, PH, FOSFORO, POTASSIO, BOMBA_ATIVA
            FROM T_REGISTROS
            ORDER BY DATA_HORA DESC
            FETCH FIRST {limit} ROWS ONLY
        """)
        
        rows = cursor.fetchall()
        return rows
    
    except Exception as e:
        print("Erro ao buscar registros dos sensores:", e)
        return []

    finally:
        cursor.close()
        conn.close()


# =============================
# CONSULTA 2 – ALERTAS_PRAGAS
# =============================
def get_alertas_pragas(limit=20):
    conn = conectar()
    if conn is None:
        return []

    try:
        cursor = conn.cursor()
        cursor.execute(f"""
            SELECT CULTURA, TEMPERATURA, UMIDADE, RISCO, RECOMENDACAO, DATA_REGISTRO, CIDADE
            FROM ALERTAS_PRAGAS
            ORDER BY DATA_REGISTRO DESC
            FETCH FIRST {limit} ROWS ONLY
        """)
        
        rows = cursor.fetchall()
        return rows
    
    except Exception as e:
        print("Erro ao buscar alertas de pragas:", e)
        return []

    finally:
        cursor.close()
        conn.close()

# =============================
# CONSULTA 3 – T_CONFIGURACOES
# =============================
def get_configuracoes():
    print("\n🔎 [DEBUG] Executando get_configuracoes()...")

    conn = conectar()
    if not conn:
        print("❌ [DEBUG] Conexão retornou None")
        return None

    try:
        cursor = conn.cursor()
        print("🔎 [DEBUG] Executando SELECT na tabela T_CONFIGURACOES...")

        cursor.execute("""
            SELECT ID_CONFIG, LIMITE_UMIDADE, PH_MIN, PH_MAX
            FROM T_CONFIGURACOES
            ORDER BY ID_CONFIG
        """)

        row = cursor.fetchone()
        print(f"📌 [DEBUG] Resultado retornado pelo banco: {row}")

        return row

    except Exception as e:
        print("❌ [ERRO] Falha ao consultar T_CONFIGURACOES:", e)
        return None

    finally:
        cursor.close()
        conn.close()
        print("🔄 [DEBUG] Conexão encerrada.")

