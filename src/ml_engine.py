import pandas as pd
from sklearn.ensemble import IsolationForest
import shap
from .db_config import get_db_client
import logging

def detect_and_explain_anomalies():
    db = get_db_client()
    
    data = list(db["car_data"].find())
    df = pd.DataFrame(data)

    
    features = ['Engine HP', 'MSRP', 'Year']
    X = df[features]

    
    model = IsolationForest(contamination=0.05, random_state=42)
    df['anomaly_score'] = model.fit_predict(X)

    
    explainer = shap.Explainer(model.predict, X)
    shap_values = explainer(X)

    
    anomalies = df[df['anomaly_score'] == -1].copy()
    
    reasons = []
    for i in anomalies.index:
        
        feature_impact = dict(zip(features, shap_values.values[i]))
        main_reason = max(feature_impact, key=feature_impact.get)
        reasons.append(f"Suspicious pattern in {main_reason}")

    anomalies['audit_reason'] = reasons

    
    db["flagged_anomalies"].delete_many({}) 
    db["flagged_anomalies"].insert_many(anomalies.to_dict("records"))
    
    logging.info(f"Audit Complete: {len(anomalies)} records flagged with SHAP explanations.")
    
