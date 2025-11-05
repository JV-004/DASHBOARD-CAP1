import oracledb
from config.settings import DB_CONFIG


def conexao_db():
    """
    Faz a conexão com o banco de dados oracle
    """
    dsn = oracledb.makedsn(DB_CONFIG['dsn'].split(':')[0], 
                        DB_CONFIG['dsn'].split(':')[1].split('/')[0], 
                        service_name=DB_CONFIG['dsn'].split('/')[1])
    return oracledb.connect(user=DB_CONFIG['user'],
                        password=DB_CONFIG['password'],
                        dsn=dsn)