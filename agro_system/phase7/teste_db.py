from db_connection import conectar

print("Testando conexão com o Oracle...")

conn = conectar()

if conn:
    print("✅ Conectado com sucesso!")
    print(conn)
    conn.close()
else:
    print("❌ Falha na conexão.")
