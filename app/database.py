from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# URL do MongoDB
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

# Conectar ao MongoDB
client = MongoClient(MONGO_URI)
db = client[DB_NAME]
urls_collection = db.urls

# Função para verificar a conexão com o banco de dados
def is_db_connected() -> bool:
    try:
        # Tentando uma simples operação de ping no banco de dados
        client.admin.command('ping')
        return True
    except Exception as e:
        return False