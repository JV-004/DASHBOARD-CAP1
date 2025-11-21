from db_connection import conectar

def inserir_alerta_praga(cultura, temperatura, umidade, risco, recomendacao, cidade):
    conn = conectar()
    if conn is None:
        return False
    
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO ALERTAS_PRAGAS 
            (CULTURA, TEMPERATURA, UMIDADE, RISCO, RECOMENDACAO, DATA_REGISTRO, CIDADE)
            VALUES (:1, :2, :3, :4, :5, SYSDATE, :6)
        """, [cultura, temperatura, umidade, risco, recomendacao, cidade])
        
        conn.commit()
        return True

    except Exception as e:
        print("Erro ao inserir alerta:", e)
        return False

    finally:
        cur.close()
        conn.close()


def listar_alertas():
    conn = conectar()
    if conn is None:
        return []
    
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM ALERTAS_PRAGAS ORDER BY DATA_REGISTRO DESC")
        resultados = cur.fetchall()
        return resultados

    except Exception as e:
        print("Erro ao consultar alertas:", e)
        return []

    finally:
        cur.close()
        conn.close()
