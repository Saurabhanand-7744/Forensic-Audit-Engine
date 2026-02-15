from fastapi import FastAPI
from src.db_config import get_db_client
import pandas as pd

app = FastAPI(title="Forensic Audit Dashboard")

@app.get("/")
def home():
    return {"status": "Online", "System": "Forensic Data Auditor API"}

@app.get("/audit-results")
def get_results(limit: int = 50):
    db = get_db_client()
    
    cursor = db["flagged_anomalies"].find({}, {"_id": 0}).limit(limit)
    data = list(cursor)
    return {"total_flagged": len(data), "records": data}

@app.get("/summary")
def get_summary():
    db = get_db_client()
    data = list(db["flagged_anomalies"].find({}, {"_id": 0}))
    df = pd.DataFrame(data)
    
    summary = df['Make'].value_counts().to_dict()
    return {"top_flagged_brands": summary}

import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("audit_engine.log"), 
        logging.StreamHandler()                
    ]
)
logger = logging.getLogger("ForensicAudit")

