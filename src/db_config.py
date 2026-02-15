import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def get_db_client():
    
    is_docker = os.path.exists('/.dockerenv')
    
   
    default_uri = "mongodb://host.docker.internal:27017/" if is_docker else "mongodb://localhost:27017/"
    
    mongo_uri = os.getenv("MONGO_URI", default_uri)
    db_name = os.getenv("DATABASE_NAME", "ForensicAuditDB")
    
    try:
        
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=2000)
        return client[db_name]
    except Exception as e:
        print(f"Database Connection Error: {e}")
        return None
