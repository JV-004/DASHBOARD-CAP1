from db_connection import conectar

conn = conectar()
cur = conn.cursor()

cur.execute("SELECT * FROM T_CONFIGURACOES")
rows = cur.fetchall()

print(rows)
