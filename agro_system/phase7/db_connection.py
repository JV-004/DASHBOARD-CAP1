import oracledb

def conectar():
    try:
        connection = oracledb.connect(
            user="RM566269",
            password="Fiap#2025",
            dsn="ORACLE.FIAP.COM.BR:1521/ORCL"
        )
        return connection
    except Exception as e:
        print("Erro ao conectar com o banco:", e)
        return None
